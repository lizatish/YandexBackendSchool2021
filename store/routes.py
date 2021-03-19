from datetime import datetime

from flask import jsonify, request

from store import app, db
from store.models.courier import Courier
from store.models.courier_assign_time import CourierAssignTime
from store.models.order import Order
from store.models.order_assign_time import OrderAssignTime


@app.route('/couriers', methods=['POST'])
def post_courier():
    couriers = request.json

    result_ids = []
    for courier in couriers['data']:
        if not Courier.query.filter_by(courier_id=courier['courier_id']).first():
            new_courier = Courier()
            new_courier.from_dict(courier)
            db.session.add(new_courier)
            db.session.commit()
            result_ids.append({'id': new_courier.courier_id})

    response = jsonify({'couriers': result_ids})
    response.status_code = 201
    return responsegit


@app.route('/couriers/<courier_id>', methods=['GET'])
def get_courier(courier_id):
    courier = Courier.query.get_or_404(courier_id)
    response = jsonify(courier.to_dict(addition_info=True))
    response.status_code = 200
    return response


@app.route('/couriers/<courier_id>', methods=['PATCH'])
def patch_courier(courier_id):
    data = request.json
    courier = Courier.query.get_or_404(courier_id)
    courier.from_dict(data)
    db.session.commit()

    response = jsonify(courier.to_dict())
    response.status_code = 200
    return response


@app.route('/orders', methods=['POST'])
def post_order():
    orders = request.json

    result_ids = []
    for order in orders['data']:
        if not Order.query.filter_by(order_id=order['order_id']).first():
            new_order = Order()
            new_order.from_dict(order)
            db.session.add(new_order)
            db.session.commit()
            result_ids.append({'id': new_order.order_id})

    response = jsonify({'orders': result_ids})
    response.status_code = 201
    return response


@app.route('/orders/assign', methods=['POST'])
def post_order_assign():
    data = request.json
    courier = Courier.query.get(data['courier_id'])

    orders = Order.query.filter(
        Order.courier_id == None,
        Order.is_complete == False,
        Order.region.in_(courier.regions)
    ).all()

    orders_idx = []
    for order in orders:
        order_assign_times = OrderAssignTime.query.filter(
            OrderAssignTime.order_id == order.order_id
        ).order_by(OrderAssignTime.time_start_hour, OrderAssignTime.time_start_min,
                   OrderAssignTime.time_finish_hour, OrderAssignTime.time_finish_min).all()

        courier_assign_times = CourierAssignTime.query.filter(
            CourierAssignTime.courier_id == courier.courier_id).all()

        for courier_time in courier_assign_times:
            for order_time in order_assign_times:
                if courier.current_weight + order.weight <= courier.max_weight:

                    if courier_time.time_start_hour >= order_time.time_finish_hour:
                        continue
                    elif order_time.time_start_hour >= courier_time.time_finish_hour:
                        continue

                    orders_idx.append({'id': order.order_id})
                    order.courier_id = courier.courier_id
                    break
                else:
                    break
            if courier.current_weight + order.weight == courier.max_weight or \
                    order.courier_id:
                break

    if orders_idx:
        db.session.commit()
        # TODO привести в правильный формат дату
        return jsonify({'orders': orders_idx, 'assign_time': datetime.utcnow()})
    return jsonify({'orders': orders_idx})


@app.route('/orders/complete', methods=['POST'])
def post_complete_assign():
    data = request.json
    order = Order.query.get(data['order_id'])
    if order.courier_id == data['courier_id']:
        order.is_complete = True
        order.complete_time = data['complete_time']
        return jsonify({'order_id': order.order_id})
    return jsonify(''), 400

from flask import jsonify, request

from store import app, db
from store.models.courier import Courier
from store.models.courier_type import CourierType
from store.models.order import Order


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
    return response


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
        # else:
        #     raise ValidationError()

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
    ).order_by(Order.time_start_hour, Order.time_start_min, Order.time_finish_hour, Order.time_finish_min).all()

    orders_idx = []
    max_weight = CourierType.max_weight(courier.courier_type)
    for order in orders:
        for courier_time in courier.assign_times:
            if order.weight < max_weight:
                if courier_time.time_start_hour <= order.time_start_hour and \
                        courier_time.time_start_min <= order.time_start_min or \
                        courier_time.time_finish_hour >= order.time_finish_hour and \
                        courier_time.time_finish_min >= order.time_finish_min:
                    orders_idx.append({'id': order.order_id})
                    order.courier_id = courier.courier_id
                break

    db.session.commit()
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
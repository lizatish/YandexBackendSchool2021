from datetime import datetime

import jsonschema
from flask import jsonify, request, abort

from store import app, db
from store.models.completed_order import CompletedOrders
from store.models.courier import Courier
from store.models.order import Order
from store.shemas.courier_id import CourierId
from store.shemas.courier_item import CourierItem
from store.shemas.courier_post_request import CouriersPostRequest
from store.shemas.order_complete import OrderComplete
from store.shemas.order_post_request import OrdersPostRequest
from store.tools import check_courier_validation


@app.route('/couriers', methods=['POST'])
def post_courier():
    couriers = request.json

    validation_errors = check_courier_validation(couriers)
    if validation_errors:
        return validation_errors

    errors_idxs = list()
    result_idxs = []
    for idx, courier in enumerate(couriers['data']):
        temp = Courier.query.get(courier['courier_id'])
        if not temp:
            new_courier = Courier()
            new_courier.from_dict(courier)
            db.session.add(new_courier)
            result_idxs.append({'id': idx + 1})
        else:
            errors_idxs.append({'id': idx + 1})

    if errors_idxs:
        return jsonify({'validation_error': {'couriers': list(errors_idxs)}}), 400

    db.session.commit()
    response = jsonify({'couriers': result_idxs})
    response.status_code = 201
    return response


@app.route('/couriers/<courier_id>', methods=['GET'])
def get_courier(courier_id):
    courier = Courier.query.get_or_404(courier_id)

    json_data = courier.to_dict()
    if courier.completed_orders:
        json_data['rating'] = courier.calculate_rating()
        json_data['earnings'] = courier.calculate_earnings()

    response = jsonify(json_data)
    response.status_code = 200
    return response


@app.route('/couriers/<courier_id>', methods=['PATCH'])
def patch_courier(courier_id):
    data = request.json

    validator = jsonschema.Draft7Validator(CourierItem)
    errors = validator.iter_errors(data)
    for error in errors:
        abort(400)

    courier = Courier.query.get(courier_id)
    if not courier:
        abort(400)

    courier.edit(data)
    orders_not_intersect = courier.check_time_not_intersection()
    for order in orders_not_intersect:
        order.courier_id = None
    db.session.commit()

    response = jsonify(courier.to_dict())
    response.status_code = 200
    return response


@app.route('/orders', methods=['POST'])
def post_order():
    orders = request.json

    validator = jsonschema.Draft7Validator(OrdersPostRequest)
    errors = validator.iter_errors(orders)
    errors_idxs = list()
    for error in errors:
        error_elem = {'id': error.path[1] + 1}
        if error_elem not in errors_idxs:
            errors_idxs.append(error_elem)
    if errors_idxs:
        return jsonify({'validation_error': {'orders': list(errors_idxs)}})

    result_ids = []
    for idx, order in enumerate(orders['data']):
        temp = Order.query.get(order['order_id'])
        if not temp:
            new_order = Order()
            new_order.from_dict(order)
            db.session.add(new_order)
            result_ids.append({'id': idx + 1})
        else:
            errors_idxs.append({'id': idx + 1})

    if errors_idxs:
        return jsonify({'validation_error': {'orders': list(errors_idxs)}})

    db.session.commit()
    response = jsonify({'orders': result_ids})
    response.status_code = 201
    return response


@app.route('/orders/assign', methods=['POST'])
def post_order_assign():
    data = request.json

    validator = jsonschema.Draft7Validator(CourierId)
    errors = list(validator.iter_errors(data))
    if errors:
        abort(400)

    courier = Courier.query.get(data['courier_id'])
    if not courier:
        abort(400)

    courier.balancer_orders()

    orders_idx = []
    orders = Order.query.filter(
        Order.courier_id == courier.courier_id,
        Order.is_complete == False
    ).all()
    assign_time = datetime.utcnow().strftime('%Y-%m-%dT%-H:%M:%S.%f'[:-3] + 'Z')
    for order in orders:
        order.assign_time = assign_time
        orders_idx.append({'id': order.order_id})

    if orders_idx:
        db.session.commit()
        return jsonify({
            'orders': orders_idx,
            'assign_time': assign_time
        })
    return jsonify({'orders': orders_idx})


@app.route('/orders/complete', methods=['POST'])
def post_complete_assign():
    data = request.json

    validator = jsonschema.Draft7Validator(OrderComplete)
    errors = list(validator.iter_errors(data))
    if errors:
        abort(400)

    order = Order.query.get(data['order_id'])
    if not order or order.courier_id != data['courier_id']:
        abort(400)

    if not order.is_complete:
        order.is_complete = True
        order.complete_time = data['complete_time']
        db.session.commit()

        complete_order = CompletedOrders.query.filter(
            CompletedOrders.courier_id == order.courier_id,
            CompletedOrders.region == order.region
        ).first()
        if not complete_order:
            complete_order = CompletedOrders(
                courier_id=order.courier_id,
                completed_orders=1,
                last_complete_time=order.complete_time,
                general_complete_seconds=(order.complete_time - order.assign_time).total_seconds(),
                region=order.region
            )
            db.session.add(complete_order)
        else:
            total_secs = (order.complete_time - complete_order.last_complete_time).total_seconds()
            complete_order.completed_orders += 1
            complete_order.last_complete_time = order.complete_time
            complete_order.general_complete_seconds += total_secs

        db.session.commit()

    return jsonify({'order_id': order.order_id}), 200

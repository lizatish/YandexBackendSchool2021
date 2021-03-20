from datetime import datetime

import jsonschema
from flask import jsonify, request, Response, abort

from store import app, db
from store.models.courier import Courier
from store.models.courier_assign_time import CourierAssignTime
from store.models.order import Order
from store.models.order_assign_time import OrderAssignTime
from store.shemas.courier_item import CourierItem
from store.shemas.courier_post_request import CouriersPostRequest
from store.shemas.order_post_request import OrdersPostRequest


@app.route('/couriers', methods=['POST'])
def post_courier():
    couriers = request.json

    validator = jsonschema.Draft7Validator(CouriersPostRequest)
    errors = validator.iter_errors(couriers)
    errors_idxs = list()
    for error in errors:
        error_elem = {'id': error.path[1] + 1}
        if error_elem not in errors_idxs:
            errors_idxs.append(error_elem)
    if errors_idxs:
        return jsonify({'validation_error': {'couriers': list(errors_idxs)}})

    result_ids = []
    for idx, courier in enumerate(couriers['data']):
        temp = Courier.query.get(courier['courier_id'])
        if not temp:
            new_courier = Courier()
            new_courier.from_dict(courier)
            db.session.add(new_courier)
            result_ids.append({'id': idx + 1})
        else:
            errors_idxs.append({'id': idx + 1})

    if errors_idxs:
        return jsonify({'validation_error': {'couriers': list(errors_idxs)}})

    db.session.commit()
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
    courier = Courier.query.get(data['courier_id'])

    orders_idx = courier.balancer_orders()
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

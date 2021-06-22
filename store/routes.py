import jsonschema
from flask import jsonify, request

from store import app
from store.shemas.courier_id import CourierId
from store.shemas.courier_item import CourierItem
from store.shemas.order_complete import OrderComplete
from store.tools.courier_service import CourierService
from store.tools.order_service import OrderService
from store.tools.time_service import TimeService
from store.tools.validation import check_error_validation


@app.route('/couriers', methods=['POST'])
def post_courier():
    couriers = request.json

    validation_errors = check_error_validation(couriers, 'courier')
    if validation_errors:
        return validation_errors

    success, errors = CourierService.add_couriers(couriers['data'])
    if errors:
        errors_idxs = list()
        error_msgs = list()
        for error_id in errors:
            errors_idxs.append({'id': error_id})
            error_msgs.append({'id': error_id, 'messages': ['Courier with this id already exist']})
        if errors_idxs:
            return jsonify({'validation_error': {'couriers': errors_idxs,
                                                 'error_description': error_msgs}}), 400

    success_idxs = list()
    for success_id in success:
        success_idxs.append({'id': success_id})
    response = jsonify({'couriers': success_idxs})
    response.status_code = 201
    return response


@app.route('/couriers/<courier_id>', methods=['GET'])
def get_courier(courier_id):
    courier = CourierService.get_courier(courier_id)
    if not courier:
        return jsonify(), 404

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
        return jsonify(), 400

    courier = CourierService.get_courier(courier_id)
    if not courier:
        return jsonify(), 404

    CourierService.edit_courier(courier, data)
    intersection_orders = CourierService.get_intersection_orders(courier)
    OrderService.release_orders(intersection_orders)

    response = jsonify(courier.to_dict())
    response.status_code = 200
    return response


@app.route('/orders', methods=['POST'])
def post_order():
    orders = request.json

    validation_errors = check_error_validation(orders, 'order')
    if validation_errors:
        return validation_errors

    success, errors = OrderService.add_orders(orders['data'])
    if errors:
        errors_idxs = list()
        error_msgs = list()
        for error_id in errors:
            errors_idxs.append({'id': error_id})
            error_msgs.append({'id': error_id, 'messages': ['Order with this id already exist']})
        if errors_idxs:
            return jsonify({'validation_error': {'orders': errors_idxs,
                                                 'error_description': error_msgs}}), 400

    success_idxs = list()
    for success_id in success:
        success_idxs.append({'id': success_id})
    response = jsonify({'orders': success_idxs})
    response.status_code = 201
    return response


#  TODO протестировать
@app.route('/orders/assign', methods=['POST'])
def post_order_assign():
    data = request.json

    validator = jsonschema.Draft7Validator(CourierId)
    errors = list(validator.iter_errors(data))
    if errors:
        return jsonify(), 400

    courier = CourierService.get_courier(data['courier_id'])
    if not courier:
        return jsonify(), 400

    new_orders, old_orders = CourierService.get_assign_orders(courier)

    if not new_orders and old_orders:
        orders_idx = []
        for order in old_orders:
            orders_idx.append({'id': order.order_id})
        return jsonify({'orders': orders_idx,
                        'assign_time':
                            TimeService.get_assign_time_from_datetime(old_orders[0].assign_time)
                        })

    orders_idx = []
    orders = OrderService.refresh_assign_time(courier)
    for order in orders:
        orders_idx.append({'id': order.order_id})

    if orders_idx:
        return jsonify({
            'orders': orders_idx,
            'assign_time': TimeService.get_assign_time_from_datetime(orders[0].assign_time)
        })
    return jsonify({'orders': orders_idx})


@app.route('/orders/complete', methods=['POST'])
def post_complete_assign():
    data = request.json

    validator = jsonschema.Draft7Validator(OrderComplete, format_checker=jsonschema.FormatChecker())
    errors = list(validator.iter_errors(data))
    if errors:
        return jsonify(), 400

    order = OrderService.get_order(data['order_id'])
    if not order or order.courier_id != data['courier_id']:
        return jsonify(), 400

    if not order.is_complete:
        OrderService.complete_order(order, data['complete_time'])

    return jsonify({'order_id': order.order_id}), 200

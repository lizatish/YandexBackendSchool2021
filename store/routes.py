import jsonschema
from flask import jsonify, request

from store import app
from store.shemas.courier_id import CourierId
from store.shemas.order_complete import OrderComplete
from store.tools.courier_service import CourierService
from store.tools.json_service import JsonService
from store.tools.order_service import OrderService
from store.tools.time_service import TimeService
from store.tools.validation import Validator


@app.route('/couriers', methods=['POST'])
def post_courier():
    json_service = JsonService()

    couriers = request.json

    errors = Validator().check_post_courier_validation(couriers)
    if errors:
        return json_service.return_validation_error_answer_400('couriers', couriers, errors)

    success, errors = CourierService.add_couriers(couriers['data'])
    if errors:
        return json_service.return_courier_logic_error_answer_400(errors)

    return json_service.return_answer_201('couriers', success)


@app.route('/couriers/<courier_id>', methods=['GET'])
def get_courier(courier_id):
    json_service = JsonService()

    courier = CourierService.get_courier(courier_id)
    if not courier:
        return json_service.return_404()

    json_data = courier.to_dict()
    return json_service.return_200(json_data)


@app.route('/couriers/<courier_id>', methods=['PATCH'])
def patch_courier(courier_id):
    json_service = JsonService()

    data = request.json

    errors = Validator().check_get_courier_validation(data)
    if errors:
        return json_service.return_400()

    courier = CourierService.get_courier(courier_id)
    if not courier:
        return json_service.return_404()

    CourierService.edit_courier(courier, data)

    return json_service.return_200(courier.to_dict())


@app.route('/orders', methods=['POST'])
def post_order():
    json_service = JsonService()

    orders = request.json

    errors = Validator().check_post_order_validation(orders)
    if errors:
        return json_service.return_validation_error_answer_400('orders', orders, errors)

    success, errors = OrderService.add_orders(orders['data'])
    if errors:
        return json_service.return_order_logic_error_answer_400(errors)

    return json_service.return_answer_201('orders', success)


@app.route('/orders/assign', methods=['POST'])
def post_order_assign():
    json_service = JsonService()

    data = request.json

    validator = jsonschema.Draft7Validator(CourierId)
    errors = list(validator.iter_errors(data))
    if errors:
        return json_service.return_400()

    courier = CourierService.get_courier(data['courier_id'])
    if not courier:
        return json_service.return_400()

    new_orders, old_orders = CourierService.get_assign_orders(courier)

    if not new_orders and old_orders:
        orders_idx = []
        for order in old_orders:
            orders_idx.append({'id': order.id})
        return jsonify({'orders': orders_idx,
                        'assign_time':
                            TimeService.get_assign_time_from_datetime(old_orders[0].assign_time)
                        })

    orders_idx = []
    orders = OrderService.refresh_assign_time(courier)
    for order in orders:
        orders_idx.append({'id': order.id})

    if orders_idx:
        return jsonify({
            'orders': orders_idx,
            'assign_time': TimeService.get_assign_time_from_datetime(orders[0].assign_time)
        })
    return jsonify({'orders': orders_idx})


@app.route('/orders/complete', methods=['POST'])
def post_complete_assign():
    json_service = JsonService()

    data = request.json

    validator = jsonschema.Draft7Validator(OrderComplete, format_checker=jsonschema.FormatChecker())
    errors = list(validator.iter_errors(data))
    if errors:
        return json_service.return_400()

    order = OrderService.get_order(data['order_id'])
    if not order or order.courier_id != data['courier_id']:
        return json_service.return_400()

    if not order.is_complete:
        OrderService.complete_order(order, data['complete_time'])

    return json_service.return_200({'order_id': order.id})

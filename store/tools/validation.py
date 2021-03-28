import jsonschema
from flask import jsonify

from store.shemas.courier_post_request import CouriersPostRequest
from store.shemas.order_post_request import OrdersPostRequest


def check_error_validation(couriers, type):
    if type == 'order':
        id_type = 'order_id'
        error_type = 'orders'
        validator = jsonschema.Draft7Validator(OrdersPostRequest)
    else:
        id_type = 'courier_id'
        error_type = 'couriers'
        validator = jsonschema.Draft7Validator(CouriersPostRequest)

    errors = validator.iter_errors(couriers)
    errors_idxs = list()
    error_msgs = list()
    for error in errors:
        if not error.path:
            error_msgs.append(error.message)
            error_elem = [{'id': elem[id_type]} for elem in couriers['data']]
            errors_idxs.append(error_elem)
            break

        id = couriers['data'][error.path[1]][id_type]
        error_elem = {'id': id}

        if error_elem not in errors_idxs:
            errors_idxs.append(error_elem)
            error_msgs.append({'id': id, 'messages': [error.message]})
        else:
            error_msgs[-1]['messages'].append(error.message)

    if errors_idxs or error_msgs:
        return jsonify({'validation_error':
                            {error_type: list(errors_idxs),
                             'error_description': error_msgs}}), 400

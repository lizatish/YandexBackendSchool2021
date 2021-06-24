from datetime import datetime

import jsonschema
from flask import jsonify

from store.shemas.courier_post_request import CouriersPostRequest
from store.shemas.order_post_request import OrdersPostRequest


def validate_data_with_time_interval(schema, instance):
    base_validator = jsonschema.Draft7Validator

    def is_time_interval(checker, inst):
        try:
            date = inst.split('-')
            if len(date) != 2:
                raise ValueError
            datetime.strptime(date[0], '%H:%M')
            datetime.strptime(date[1], '%H:%M')
            return True
        except ValueError:
            return False

    interval_time_check = base_validator.TYPE_CHECKER.redefine(u'interval_time', is_time_interval)
    validator = jsonschema.validators.extend(jsonschema.Draft7Validator, type_checker=interval_time_check)
    return validator(schema=schema).iter_errors(instance)


def create_error_message(data_type, data, errors):
    errors_idxs = list()
    error_msgs = list()
    for error in errors:
        if len(error.path) < 2:
            error_msgs.append(error.message)
            break

        error_data_elem = data['data'][error.path[1]]
        if data_type == 'couriers' and 'courier_id' in error_data_elem:
            id = error_data_elem['courier_id']
        elif data_type == 'orders' and 'order_id' in error_data_elem:
            id = error_data_elem['order_id']
        else:
            id = error.path[1] + 1
        error_id = {'id': id}

        if error_id not in errors_idxs:
            errors_idxs.append(error_id)
            error_msgs.append({'id': id, 'messages': [error.message]})
        else:
            error_msgs[-1]['messages'].append(error.message)

    if errors_idxs or error_msgs:
        return jsonify({'validation_error':
                            {data_type: list(errors_idxs),
                             'error_description': error_msgs}}), 400


def check_courier_validation(data):
    errors = validate_data_with_time_interval(CouriersPostRequest, data)
    if errors:
        return create_error_message('couriers', data, errors)


def check_order_validation(data):
    errors = validate_data_with_time_interval(OrdersPostRequest, data)
    if errors:
        return create_error_message('orders', data, errors)

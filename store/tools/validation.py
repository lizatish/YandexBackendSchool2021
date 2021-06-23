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


def create_error_message(data, errors, id_type, data_type):
    errors_idxs = list()
    error_msgs = list()
    for error in errors:
        if not error.path:
            error_msgs.append(error.message)
            error_elem = [{'id': elem[id_type]} for elem in data['data']]
            errors_idxs.append(error_elem)
            break

        id = data['data'][error.path[1]][id_type]
        error_elem = {'id': id}

        if error_elem not in errors_idxs:
            errors_idxs.append(error_elem)
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
        return create_error_message(data, errors, 'courier_id', 'couriers')


def check_order_validation(data):
    errors = validate_data_with_time_interval(OrdersPostRequest, data)
    if errors:
        return create_error_message(data, errors, 'order_id', 'orders')

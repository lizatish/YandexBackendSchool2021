from datetime import datetime

import jsonschema

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
    return list(validator(schema=schema).iter_errors(instance))


def check_courier_validation(data):
    errors = validate_data_with_time_interval(CouriersPostRequest, data)
    return errors



def check_order_validation(data):
    errors = validate_data_with_time_interval(OrdersPostRequest, data)
    if errors:
        return create_error_message('orders', data, errors)

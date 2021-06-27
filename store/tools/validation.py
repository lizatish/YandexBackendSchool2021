from datetime import datetime

import jsonschema

from store.shemas.courier_item import CourierItem
from store.shemas.courier_post_request import CouriersPostRequest
from store.shemas.order_post_request import OrdersPostRequest


class Validator:
    def check_post_courier_validation(self, data):
        errors = self.__validate_data_with_time_interval(CouriersPostRequest, data)
        return errors

    def check_post_order_validation(self, data):
        errors = self.__validate_data_with_time_interval(OrdersPostRequest, data)
        return errors

    def check_get_courier_validation(self, data):
        errors = self.__validate_data_with_time_interval(CourierItem, data)
        return errors

    def __create_base_validator(self, data, schema):
        validator = jsonschema.Draft7Validator(schema)
        return validator.iter_errors(data)

    def __validate_data_with_time_interval(self, schema, instance):
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

import jsonschema
from flask import jsonify

from store.shemas.courier_post_request import CouriersPostRequest


def check_courier_validation(couriers):
    validator = jsonschema.Draft7Validator(CouriersPostRequest)
    errors = validator.iter_errors(couriers)
    errors_idxs = list()
    error_msgs = list()
    for error in errors:
        if not error.path:
            error_msgs.append(error.message)
            error_elem = [{'id': elem['courier_id']} for elem in couriers['data']]
            errors_idxs.append(error_elem)
            break

        courier_id = couriers['data'][error.path[1]]['courier_id']
        error_elem = {'id': courier_id}

        if error_elem not in errors_idxs:
            errors_idxs.append(error_elem)
            error_msgs.append({'id': courier_id, 'messages': [error.message]})
        else:
            error_msgs[-1]['messages'].append(error.message)

    if errors_idxs or error_msgs:
        return jsonify({'validation_error':
                            {'couriers': list(errors_idxs),
                             'error_description': error_msgs}}), 400

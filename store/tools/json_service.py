from flask import jsonify


class JsonService:
    def __form_400(self, data_type, errors_idxs, error_msgs):
        return jsonify({'validation_error': {data_type: errors_idxs,
                                             'error_description': error_msgs}}), 400

    def return_courier_answer_201(self, success):
        success_idxs = list()
        for success_id in success:
            success_idxs.append({'id': success_id})
        response = jsonify({'couriers': success_idxs})
        response.status_code = 201
        return response

    def return_courier_logic_error_answer_400(self, errors):
        errors_idxs = list()
        error_msgs = list()
        for error_id in errors:
            errors_idxs.append({'id': error_id})
            error_msgs.append({'id': error_id, 'messages': ['Courier with this id already exist']})

        return self.__form_400('couriers', errors_idxs, error_msgs)

    def return_validation_error_answer_400(self, data_type, data, errors):
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

        return self.__form_400(data_type, errors_idxs, error_msgs)

    def answer_200(self):
        pass

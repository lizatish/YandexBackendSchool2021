from flask import jsonify, request

from store import app


@app.route('/couriers', methods=['POST'])
def couriers():
    content = request.json
    if content:
        reference = content.get('schema').get('$ref')  # todo: проверить так ли забирается ссылка

        if reference:
            content = {
                'schema': {'$ref': '#/components/schemas/CouriersIds'}
            }
            response = jsonify(content)
            response.status_code = 200
            response.status = 'Created'  # тут должно быть дескрипшн
            response.mimetype = 'application/json'
            return response

    content = {
        'type': 'object',
        'additionalProperties': 'false',
        'properties':
            {'validation_error':
                 {'$ref': '#/components/schemas/CouriersIds'}},
        'schema': {'$ref': '#/components/schemas/CouriersIds'},
        'required': 'validation_error'
    }
    response = jsonify(content)
    response.status_code = 400
    response.status = 'Bad request'  # тут должно быть дескрипшн
    response.mimetype = 'application/json'
    return response

@app.route('/couriers/{courier_id}', methods=['GET'])
def api_couriers_get(courier_id):
    path = request.args.get('in')
    name = request.args.get('courier_id')
    required = request.args.get('true')
    schema_type = request.args.get('schema').get('type')



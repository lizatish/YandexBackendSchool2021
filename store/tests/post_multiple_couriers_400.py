import requests

url = 'http://127.0.0.1:5000/couriers'


def check_two_elements_base_400(input, output, first_message_count, second_message_count):
    assert output.status_code == 400
    json_response = output.json()
    validation_error = json_response.get('validation_error')
    assert validation_error is not None
    assert len(validation_error) == 2

    couriers = validation_error.get('couriers')
    assert couriers is not None
    assert len(couriers) == 2
    assert couriers[0].get('id') == input['data'][0]['courier_id']
    assert couriers[1].get('id') == input['data'][1]['courier_id']

    description = validation_error.get('error_description')
    assert description is not None
    assert len(description) == 2

    assert description[0].get('id') == input['data'][0]['courier_id']
    messages = description[0].get('messages')
    assert messages is not None
    assert len(messages) == first_message_count

    assert description[1].get('id') == input['data'][1]['courier_id']
    messages = description[0].get('messages')
    assert messages is not None
    assert len(messages) == second_message_count


def test_mult_validation_error1_couriers():
    json = {
        "data": [
            {
                "courier_id": 1,
                "123123": 1,
                "courier_type": "car",
                "regions": [1, 12, 22],
                "working_hours": ["11:005-14:05"]
            },
            {
                "courier_id": 2,
                "123123": 1,
                "courier_type": "car",
                "regions": [1, 12, 22],
                "working_hours": ["11:005-14:05"]
            }
        ]
    }
    response = requests.post(url=url, json=json)
    check_two_elements_base_400(json, response, 2, 2)

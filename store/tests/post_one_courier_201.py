import pytest
import requests

from store.models.courier import Courier

url = 'http://127.0.0.1:5000/couriers'


def check_base_400(input, output, messages_num):
    assert output.status_code == 400
    json_response = output.json()
    validation_error = json_response.get('validation_error')
    assert validation_error is not None
    assert len(validation_error) == 2

    couriers = validation_error.get('couriers')
    assert couriers is not None
    assert len(couriers) == 1
    assert couriers[0].get('id') == input['data'][0]['courier_id']

    description = validation_error.get('error_description')
    assert description is not None
    assert len(description) == 1
    assert description[0].get('id') == input['data'][0]['courier_id']

    messages = description[0].get('messages')
    assert messages is not None
    assert len(messages) == messages_num


def test_validation_error1_couriers(app):
    json = {
        "data": [
            {
                "courier_id": 1,
                "courier_type": "foot",
                "regions": [1, 12, 22],
                "working_hours": ["11:35-14:05", "09:00-11:00"]
            }
        ]
    }
    response = requests.post(url=url, json=json)

    assert response.status_code == 201
    json_response = response.json()
    couriers = json_response.get('couriers')
    assert couriers is not None
    assert len(couriers) == 1
    assert couriers[0].get('id') == json['data'][0]['courier_id']

    user = Courier.query.get(courier_id=json['data'][0]['courier_id'])
    assert user is not None
    assert user.courier_id == json['data'][0]['courier_id']
    assert user.courier_type == json['data'][0]['courier_type']
    for elem in user.regions:
        assert elem in json['data'][0]['regions']
    for elem in user.working_hours:
        assert elem in json['data'][0]['working_hours']

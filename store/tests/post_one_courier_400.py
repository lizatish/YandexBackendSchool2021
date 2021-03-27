import requests

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


def test_validation_error1_couriers():
    json = {
        "data": [
            {
                "courier_id": 1,
                "regions": [1, 12, 22],
                "working_hours": ["11:35-14:05", "09:00-11:00"]
            }
        ]
    }
    response = requests.post(url=url, json=json)
    check_base_400(json, response, 1)


def test_validation_error2_couriers():
    json = {
        "data": [
            {
                "courier_id": 2,
                "courier_type": "foot",
                "working_hours": ["11:35-14:05", "09:00-11:00"]
            }
        ]
    }
    response = requests.post(url=url, json=json)
    check_base_400(json, response, 1)


def test_validation_error3_couriers():
    json = {
        "data": [
            {
                "courier_id": 3,
                "courier_type": "foot",
                "regions": [1, 12, 22],
            }
        ]
    }
    response = requests.post(url=url, json=json)
    check_base_400(json, response, 1)


def test_validation_error4_couriers():
    json = {
        "data": [
            {
                "courier_id": -1,
                "courier_type": "car",
                "regions": [1, 12, 22],
                "working_hours": ["11:35-14:05", "09:00-11:00"]
            }
        ]
    }
    response = requests.post(url=url, json=json)
    check_base_400(json, response, 1)


def test_validation_error5_couriers():
    json = {
        "data": [
            {
                "courier_id": '1',
                "courier_type": "car",
                "regions": [1, 12, 22],
                "working_hours": ["11:35-14:05", "09:00-11:00"]
            }
        ]
    }
    response = requests.post(url=url, json=json)
    check_base_400(json, response, 1)


def test_validation_error6_couriers():
    json = {
        "data": [
            {
                "courier_id": 1.12,
                "courier_type": "car",
                "regions": [1, 12, 22],
                "working_hours": ["11:35-14:05", "09:00-11:00"]
            }
        ]
    }
    response = requests.post(url=url, json=json)
    check_base_400(json, response, 1)


def test_validation_error7_couriers():
    json = {
        "data": [
            {
                "courier_id": [1],
                "courier_type": "car",
                "regions": [1, 12, 22],
                "working_hours": ["11:35-14:05", "09:00-11:00"]
            }
        ]
    }
    response = requests.post(url=url, json=json)
    check_base_400(json, response, 1)


def test_validation_error8_couriers():
    json = {
        "data": [
            {
                "courier_id": 1,
                "courier_type": "carr",
                "regions": [1, 12, 22],
                "working_hours": ["11:35-14:05", "09:00-11:00"]
            }
        ]
    }
    response = requests.post(url=url, json=json)
    check_base_400(json, response, 1)


def test_validation_error9_couriers():
    json = {
        "data": [
            {
                "courier_id": 1,
                "courier_type": 1,
                "regions": [1, 12, 22],
                "working_hours": ["11:35-14:05", "09:00-11:00"]
            }
        ]
    }
    response = requests.post(url=url, json=json)
    check_base_400(json, response, 2)


def test_validation_error10_couriers():
    json = {
        "data": [
            {
                "courier_id": 1,
                "courier_type": 1.0,
                "regions": [1, 12, 22],
                "working_hours": ["11:35-14:05", "09:00-11:00"]
            }
        ]
    }
    response = requests.post(url=url, json=json)
    check_base_400(json, response, 2)


def test_validation_error11_couriers():
    json = {
        "data": [
            {
                "courier_id": 1,
                "courier_type": '',
                "regions": [1, 12, 22],
                "working_hours": ["11:35-14:05", "09:00-11:00"]
            }
        ]
    }
    response = requests.post(url=url, json=json)
    check_base_400(json, response, 1)


def test_validation_error12_couriers():
    json = {
        "data": [
            {
                "courier_id": 1,
                "courier_type": "car",
                "regions": 1,
                "working_hours": ["11:35-14:05", "09:00-11:00"]
            }
        ]
    }
    response = requests.post(url=url, json=json)
    check_base_400(json, response, 1)


def test_validation_error13_couriers():
    json = {
        "data": [
            {
                "courier_id": 1,
                "courier_type": "car",
                "regions": ['2'],
                "working_hours": ["11:35-14:05", "09:00-11:00"]
            }
        ]
    }
    response = requests.post(url=url, json=json)
    check_base_400(json, response, 1)


def test_validation_error14_couriers():
    json = {
        "data": [
            {
                "courier_id": 1,
                "courier_type": "car",
                "regions": [1, -12, 22],
                "working_hours": ["11:35-14:05", "09:00-11:00"]
            }
        ]
    }
    response = requests.post(url=url, json=json)
    check_base_400(json, response, 1)


def test_validation_error15_couriers():
    json = {
        "data": [
            {
                "courier_id": 1,
                "courier_type": "car",
                "regions": [],
                "working_hours": ["11:35-14:05", "09:00-11:00"]
            }
        ]
    }
    response = requests.post(url=url, json=json)
    check_base_400(json, response, 1)


def test_validation_error16_couriers():
    json = {
        "data": [
            {
                "courier_id": 1,
                "courier_type": "car",
                "regions": [1.1, 12, 22],
                "working_hours": ["11:35-14:05"]
            }
        ]
    }
    response = requests.post(url=url, json=json)
    check_base_400(json, response, 1)


def test_validation_error17_couriers():
    json = {
        "data": [
            {
                "courier_id": 1,
                "courier_type": "car",
                "regions": [1, 12, 22],
                "working_hours": "11:35-14:08"
            }
        ]
    }
    response = requests.post(url=url, json=json)
    check_base_400(json, response, 1)


def test_validation_error18_couriers():
    json = {
        "data": [
            {
                "courier_id": 1,
                "courier_type": "car",
                "regions": [1, 12, 22],
                "working_hours": ["11-35-14:05"]
            }
        ]
    }
    response = requests.post(url=url, json=json)
    check_base_400(json, response, 1)


def test_validation_error19_couriers():
    json = {
        "data": [
            {
                "courier_id": 1,
                "courier_type": "car",
                "regions": [1, 12, 22],
                "working_hours": ["11:35*14:05"]
            }
        ]
    }
    response = requests.post(url=url, json=json)
    check_base_400(json, response, 1)


def test_validation_error20_couriers():
    json = {
        "data": [
            {
                "courier_id": 1,
                "courier_type": "car",
                "regions": [1, 12, 22],
                "working_hours": ["11:35-14*05"]
            }
        ]
    }
    response = requests.post(url=url, json=json)
    check_base_400(json, response, 1)


def test_validation_error21_couriers():
    json = {
        "data": [
            {
                "courier_id": 1,
                "courier_type": "car",
                "regions": [1, 12, 22],
                "working_hours": ["81:35-14:05"]
            }
        ]
    }
    response = requests.post(url=url, json=json)
    check_base_400(json, response, 1)


def test_validation_error22_couriers():
    json = {
        "data": [
            {
                "courier_id": 1,
                "courier_type": "car",
                "regions": [1, 12, 22],
                "working_hours": ["11:95-14:05"]
            }
        ]
    }
    response = requests.post(url=url, json=json)
    check_base_400(json, response, 1)


def test_validation_error23_couriers():
    json = {
        "data": [
            {
                "courier_id": 1,
                "courier_type": "car",
                "regions": [1, 12, 22],
                "working_hours": ["11:05-94:05"]
            }
        ]
    }
    response = requests.post(url=url, json=json)
    check_base_400(json, response, 1)


def test_validation_error24_couriers():
    json = {
        "data": [
            {
                "courier_id": 1,
                "courier_type": "car",
                "regions": [1, 12, 22],
                "working_hours": ["11:05-14:95"]
            }
        ]
    }
    response = requests.post(url=url, json=json)
    check_base_400(json, response, 1)


def test_validation_error25_couriers():
    json = {
        "data": [
            {
                "courier_id": 1,
                "courier_type": "car",
                "regions": [1, 12, 22],
                "working_hours": ["11:05-14:005"]
            }
        ]
    }
    response = requests.post(url=url, json=json)
    check_base_400(json, response, 1)


def test_validation_error26_couriers():
    json = {
        "data": [
            {
                "courier_id": 1,
                "courier_type": "car",
                "regions": [1, 12, 22],
                "working_hours": ["11:005-14:05"]
            }
        ]
    }
    response = requests.post(url=url, json=json)
    check_base_400(json, response, 1)


def test_validation_error27_couriers():
    json = {
        "data": [
            {
                "courier_id": 1,
                "123123": 1,
                "courier_type": "car",
                "regions": [1, 12, 22],
                "working_hours": ["11:05-14:05"]
            }
        ]
    }
    response = requests.post(url=url, json=json)
    check_base_400(json, response, 1)

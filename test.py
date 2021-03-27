import requests

url = 'http://127.0.0.1:5000/couriers'


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
    assert response.status_code == 400

    json_response = response.json()
    validation_error = json_response.get('validation_error')
    assert validation_error is not None
    assert len(validation_error) == 1

    couriers = validation_error.get('couriers')
    assert len(couriers) == 1
    assert couriers[0].get('id') == json['data'][0]['courier_id']


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
    assert response.status_code == 400

    json_response = response.json()
    validation_error = json_response.get('validation_error')
    assert validation_error is not None
    assert len(validation_error) == 1

    couriers = validation_error.get('couriers')
    assert len(couriers) == 1
    assert couriers[0].get('id') == json['data'][0]['courier_id']


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
    assert response.status_code == 400

    json_response = response.json()
    validation_error = json_response.get('validation_error')
    assert validation_error is not None
    assert len(validation_error) == 1

    couriers = validation_error.get('couriers')
    assert len(couriers) == 1
    assert couriers[0].get('id') == json['data'][0]['courier_id']


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
    assert response.status_code == 400

    json_response = response.json()
    validation_error = json_response.get('validation_error')
    assert validation_error is not None
    assert len(validation_error) == 1

    couriers = validation_error.get('couriers')
    assert len(couriers) == 1
    assert couriers[0].get('id') == json['data'][0]['courier_id']


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
    assert response.status_code == 400

    json_response = response.json()
    validation_error = json_response.get('validation_error')
    assert validation_error is not None
    assert len(validation_error) == 1

    couriers = validation_error.get('couriers')
    assert len(couriers) == 1
    assert couriers[0].get('id') == json['data'][0]['courier_id']


def test_validation_error6_couriers():
    json = {
        "data": [
            {
                "courier_id": 1.000,
                "courier_type": "car",
                "regions": [1, 12, 22],
                "working_hours": ["11:35-14:05", "09:00-11:00"]
            }
        ]
    }
    response = requests.post(url=url, json=json)
    assert response.status_code == 400

    json_response = response.json()
    validation_error = json_response.get('validation_error')
    assert validation_error is not None
    assert len(validation_error) == 1

    couriers = validation_error.get('couriers')
    assert len(couriers) == 1
    assert couriers[0].get('id') == json['data'][0]['courier_id']


def test_validation_error7_couriers():
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
    assert response.status_code == 400

    json_response = response.json()
    validation_error = json_response.get('validation_error')
    assert validation_error is not None
    assert len(validation_error) == 1

    couriers = validation_error.get('couriers')
    assert len(couriers) == 1
    assert couriers[0].get('id') == json['data'][0]['courier_id']


def test_validation_error8_couriers():
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
    assert response.status_code == 400

    json_response = response.json()
    validation_error = json_response.get('validation_error')
    assert validation_error is not None
    assert len(validation_error) == 1

    couriers = validation_error.get('couriers')
    assert len(couriers) == 1
    assert couriers[0].get('id') == json['data'][0]['courier_id']


def test_validation_error9_couriers():
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
    assert response.status_code == 400

    json_response = response.json()
    validation_error = json_response.get('validation_error')
    assert validation_error is not None
    assert len(validation_error) == 1

    couriers = validation_error.get('couriers')
    assert len(couriers) == 1
    assert couriers[0].get('id') == json['data'][0]['courier_id']


def test_validation_error10_couriers():
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
    assert response.status_code == 400

    json_response = response.json()
    validation_error = json_response.get('validation_error')
    assert validation_error is not None
    assert len(validation_error) == 1

    couriers = validation_error.get('couriers')
    assert len(couriers) == 1
    assert couriers[0].get('id') == json['data'][0]['courier_id']


def test_validation_error11_couriers():
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
    assert response.status_code == 400

    json_response = response.json()
    validation_error = json_response.get('validation_error')
    assert validation_error is not None
    assert len(validation_error) == 1

    couriers = validation_error.get('couriers')
    assert len(couriers) == 1
    assert couriers[0].get('id') == json['data'][0]['courier_id']


def test_validation_error12_couriers():
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
    assert response.status_code == 400

    json_response = response.json()
    validation_error = json_response.get('validation_error')
    assert validation_error is not None
    assert len(validation_error) == 1

    couriers = validation_error.get('couriers')
    assert len(couriers) == 1
    assert couriers[0].get('id') == json['data'][0]['courier_id']


def test_validation_error13_couriers():
    json = {
        "data": [
            {
                "courier_id": 1,
                "courier_type": "car",
                "regions": [1, 12, 22],
                "working_hours": "11:35-14:05"
            }
        ]
    }
    response = requests.post(url=url, json=json)
    assert response.status_code == 400

    json_response = response.json()
    validation_error = json_response.get('validation_error')
    assert validation_error is not None
    assert len(validation_error) == 1

    couriers = validation_error.get('couriers')
    assert len(couriers) == 1
    assert couriers[0].get('id') == json['data'][0]['courier_id']


def test_validation_error14_couriers():
    json = {
        "data": [
            {
                "courier_id": 1,
                "courier_type": "car",
                "regions": [1.0, 12, 22],
                "working_hours": ["11:35-14:05"]
            }
        ]
    }
    response = requests.post(url=url, json=json)
    assert response.status_code == 400

    json_response = response.json()
    validation_error = json_response.get('validation_error')
    assert validation_error is not None
    assert len(validation_error) == 1

    couriers = validation_error.get('couriers')
    assert len(couriers) == 1
    assert couriers[0].get('id') == json['data'][0]['courier_id']


def test_validation_error15_couriers():
    json = {
        "data": [
            {
                "courier_id": 1,
                "courier_type": "car",
                "regions": [1, 12, 22],
                "working_hours": ["11:35-14:058"]
            }
        ]
    }
    response = requests.post(url=url, json=json)
    assert response.status_code == 400

    json_response = response.json()
    validation_error = json_response.get('validation_error')
    assert validation_error is not None
    assert len(validation_error) == 1

    couriers = validation_error.get('couriers')
    assert len(couriers) == 1
    assert couriers[0].get('id') == json['data'][0]['courier_id']


def test_validation_error16_couriers():
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
    assert response.status_code == 400

    json_response = response.json()
    validation_error = json_response.get('validation_error')
    assert validation_error is not None
    assert len(validation_error) == 1

    couriers = validation_error.get('couriers')
    assert len(couriers) == 1
    assert couriers[0].get('id') == json['data'][0]['courier_id']


def test_validation_error17_couriers():
    json = {
        "data": [
            {
                "courier_id": 1,
                "courier_type": "car",
                "regions": [1, 12, 22],
                "working_hours": ["45:36-14:05"]
            }
        ]
    }
    response = requests.post(url=url, json=json)
    assert response.status_code == 400

    json_response = response.json()
    validation_error = json_response.get('validation_error')
    assert validation_error is not None
    assert len(validation_error) == 1

    couriers = validation_error.get('couriers')
    assert len(couriers) == 1
    assert couriers[0].get('id') == json['data'][0]['courier_id']


def test_validation_error18_couriers():
    json = {
        "data": [
            {
                "courier_id": 1,
                "courier_type": "car",
                "regions": [1, 12, 22],
                "working_hours": ["11:90-14:05"]
            }
        ]
    }

    response = requests.post(url=url, json=json)
    assert response.status_code == 400

    json_response = response.json()
    validation_error = json_response.get('validation_error')
    assert validation_error is not None
    assert len(validation_error) == 1

    couriers = validation_error.get('couriers')
    assert len(couriers) == 1
    assert couriers[0].get('id') == json['data'][0]['courier_id']


def test_validation_error19_couriers():
    json = {
        "data": [
            {
                "courier_id": 1,
                "courier_type": "car",
                "regions": [1, 12, 22],
                "working_hours": ["11:45-90:05"]
            }
        ]
    }

    response = requests.post(url=url, json=json)
    assert response.status_code == 400

    json_response = response.json()
    validation_error = json_response.get('validation_error')
    assert validation_error is not None
    assert len(validation_error) == 1

    couriers = validation_error.get('couriers')
    assert len(couriers) == 1
    assert couriers[0].get('id') == json['data'][0]['courier_id']


def test_validation_error20_couriers():
    json = {
        "data": [
            {
                "courier_id": 1,
                "courier_type": "car",
                "regions": [1, 12, 22],
                "working_hours": ["11:45-12:90"]
            }
        ]
    }

    response = requests.post(url=url, json=json)
    assert response.status_code == 400

    json_response = response.json()
    validation_error = json_response.get('validation_error')
    assert validation_error is not None
    assert len(validation_error) == 1

    couriers = validation_error.get('couriers')
    assert len(couriers) == 1
    assert couriers[0].get('id') == json['data'][0]['courier_id']


def test_validation_error21_couriers():
    json = {
        "data": [
            {
                "courier_id": 1,
                "courier_type": "car",
                "regions": [1, 12, 22],
                "working_hours": ["11:45-12-05"]
            }
        ]
    }
    response = requests.post(url=url, json=json)
    assert response.status_code == 400

    json_response = response.json()
    validation_error = json_response.get('validation_error')
    assert validation_error is not None
    assert len(validation_error) == 1

    couriers = validation_error.get('couriers')
    assert len(couriers) == 1
    assert couriers[0].get('id') == json['data'][0]['courier_id']


def test_validation_error22_couriers():
    json = {
        "data": [
            {
                "courier_id": 1,
                "courier_type": "car",
                "regions": [1, 12, 22],
                "working_hours": ["11:45-12-05"]
            }
        ]
    }

    response = requests.post(url=url, json=json)
    assert response.status_code == 400

    json_response = response.json()
    validation_error = json_response.get('validation_error')
    assert validation_error is not None
    assert len(validation_error) == 1

    couriers = validation_error.get('couriers')
    assert len(couriers) == 1
    assert couriers[0].get('id') == json['data'][0]['courier_id']


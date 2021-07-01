import json

from store.main.models.courier import Courier
from store.main.models.courier_type import CourierType

BASE_URL = 'http://0.0.0.0:8081/couriers'
METHOD = 'POST'


def test_valid_login_logout(test_client):
    data = {
        "data": [
            {
                "courier_id": 1,
                "courier_type": "foot",
                "regions": [1, 12, 22],
                "working_hours": ["11:35-14:05", "09:00-11:00"]
            }
        ]
    }

    response = test_client.post('/couriers', headers={"Content-Type": "application/json"},
                           data=json.dumps(data))
    assert response.status_code == 201


def test_post_one_courier(test_client):
    data = {
        "data": [
            {
                "courier_id": 1,
                "courier_type": "foot",
                "regions": [1, 12, 22],
                "working_hours": ["11:35-14:05", "09:00-11:00"]
            }
        ]
    }

    response = test_client.post('/couriers', headers={"Content-Type": "application/json"},
                           data=json.dumps(data))
    assert response.status_code == 201

    courier = Courier.query.get(1)
    assert courier is not None
    assert courier.courier_type == CourierType.FOOT
    assert courier.regions == [1, 12, 22]
    assert courier.get_working_hours() == ["11:35-14:05", "09:00-11:00"]

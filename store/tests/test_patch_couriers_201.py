import json

from store.main.models.courier import Courier
from store.main.models.courier_type import CourierType

HEADERS = {"Content-Type": "application/json"}


def get_route(id):
    return f'/couriers/{id}'


def test_patch_courier_type(test_client):
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
    _ = test_client.post('couriers', headers=HEADERS, data=json.dumps(data))

    data = {
        "courier_type": "car"
    }
    response = test_client.patch(get_route(1), headers=HEADERS, data=json.dumps(data))
    assert response.status_code == 200

    courier = Courier.query.get(1)
    assert courier.courier_type == CourierType.CAR
    assert courier.regions == [1, 12, 22]
    assert courier.get_working_hours() == ["11:35-14:05", "09:00-11:00"]


def test_patch_regions(test_client):
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
    _ = test_client.post('couriers', headers=HEADERS, data=json.dumps(data))

    data = {
        "regions": [1, 12, 22, 33]
    }
    response = test_client.patch(get_route(1), headers=HEADERS, data=json.dumps(data))
    assert response.status_code == 200

    courier = Courier.query.get(1)
    assert courier.courier_type == CourierType.FOOT
    assert courier.regions == [1, 12, 22, 33]
    assert courier.get_working_hours() == ["11:35-14:05", "09:00-11:00"]


def test_patch_working_hours(test_client):
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
    _ = test_client.post('couriers', headers=HEADERS, data=json.dumps(data))

    data = {
        "working_hours": ["08:00-13:00"]
    }
    response = test_client.patch(get_route(1), headers=HEADERS, data=json.dumps(data))
    assert response.status_code == 200

    courier = Courier.query.get(1)
    assert courier.courier_type == CourierType.FOOT
    assert courier.regions == [1, 12, 22]
    assert courier.get_working_hours() == ["08:00-13:00"]

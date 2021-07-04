import json

from store.main.models.courier import Courier
from store.main.models.courier_type import CourierType

HEADERS = {"Content-Type": "application/json"}
ROUTE = '/couriers'


def test_post_one_courier_post_one_courier_base_data(test_client):
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

    response = test_client.post(ROUTE, headers=HEADERS, data=json.dumps(data))
    assert response.status_code == 201

    courier = Courier.query.get(1)
    assert courier.courier_type == CourierType.FOOT
    assert courier.regions == [1, 12, 22]
    assert courier.get_working_hours() == ["11:35-14:05", "09:00-11:00"]


def test_post_one_courier_check_init_foot_courier_type(test_client):
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

    response = test_client.post(ROUTE, headers=HEADERS, data=json.dumps(data))
    assert response.status_code == 201

    courier = Courier.query.get(1)
    assert courier.courier_type == CourierType.FOOT
    assert courier.current_weight == 0
    assert courier.max_weight == 10


def test_post_one_courier_check_init_bike_courier_type(test_client):
    data = {
        "data": [
            {
                "courier_id": 1,
                "courier_type": "bike",
                "regions": [1, 12, 22],
                "working_hours": ["11:35-14:05", "09:00-11:00"]
            }
        ]
    }

    response = test_client.post(ROUTE, headers=HEADERS, data=json.dumps(data))
    assert response.status_code == 201

    courier = Courier.query.get(1)
    assert courier.courier_type == CourierType.BIKE
    assert courier.current_weight == 0
    assert courier.max_weight == 15


def test_post_one_courier_check_init_car_courier_type(test_client):
    data = {
        "data": [
            {
                "courier_id": 1,
                "courier_type": "car",
                "regions": [1, 12, 22],
                "working_hours": ["11:35-14:05", "09:00-11:00"]
            }
        ]
    }

    response = test_client.post(ROUTE, headers=HEADERS, data=json.dumps(data))
    assert response.status_code == 201

    courier = Courier.query.get(1)
    assert courier.courier_type == CourierType.CAR
    assert courier.current_weight == 0
    assert courier.max_weight == 50


def test_post_one_courier_check_init_courier_id(test_client):
    data = {
        "data": [
            {
                "courier_id": 1,
                "courier_type": "car",
                "regions": [1, 12, 22],
                "working_hours": ["11:35-14:05", "09:00-11:00"]
            }
        ]
    }

    response = test_client.post(ROUTE, headers=HEADERS, data=json.dumps(data))
    assert response.status_code == 201

    courier1 = Courier.query.get(1)
    courier2 = Courier.query.get(1)
    assert courier1 == courier2


def test_post_multiple_couriers(test_client):
    data = {
        "data": [
            {
                "courier_id": 1,
                "courier_type": "car",
                "regions": [1, 12, 22],
                "working_hours": ["11:35-14:05", "09:00-11:00"]
            },
            {
                "courier_id": 2,
                "courier_type": "bike",
                "regions": [1],
                "working_hours": ["12:35-14:05"]
            }
        ]
    }

    response = test_client.post(ROUTE, headers=HEADERS, data=json.dumps(data))
    assert response.status_code == 201

    courier = Courier.query.get(1)
    assert courier.courier_type == CourierType.CAR
    assert courier.regions == [1, 12, 22]
    assert courier.get_working_hours() == ["11:35-14:05", "09:00-11:00"]

    courier = Courier.query.get(2)
    assert courier.courier_type == CourierType.BIKE
    assert courier.regions == [1]
    assert courier.get_working_hours() == ["12:35-14:05"]

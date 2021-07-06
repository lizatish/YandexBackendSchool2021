import ast
import json

from store.main.models.courier import Courier
from store.main.models.order import Order

HEADERS = {"Content-Type": "application/json"}


def test_complete_one_valid_order_courier_type_foot(test_client):
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
    _ = test_client.post('couriers', headers=HEADERS, data=json.dumps(data))
    data = {
        "data": [
            {
                "order_id": 1,
                "weight": 8,
                "region": 12,
                "delivery_hours": ["09:00-18:00"]
            },
            {
                "order_id": 2,
                "weight": 6,
                "region": 12,
                "delivery_hours": ["09:00-18:00"]
            },
            {
                "order_id": 3,
                "weight": 1,
                "region": 12,
                "delivery_hours": ["09:00-18:00"]
            }
        ]
    }
    _ = test_client.post('orders', headers=HEADERS, data=json.dumps(data))

    data = {
        "courier_id": 1
    }
    response = test_client.post('orders/assign', headers=HEADERS, data=json.dumps(data))
    assert response.status_code == 200
    data = ast.literal_eval(response.data.decode("UTF-8"))
    assert len(data) == 2
    assert len(data.get('orders')) == 3

    # courier = Courier.query.get(1)
    # assert courier.max_weight == 15
    # assert courier.current_weight == 15

    #  САМ ТЕСТ ОТСЮДА
    data = {
        "courier_type": "foot"
    }
    response = test_client.patch('couriers/1', headers=HEADERS, data=json.dumps(data))
    assert response.status_code == 200

    courier = Courier.query.get(1)
    assert courier.max_weight == 10
    assert courier.current_weight == 7
    assert len(courier.orders) == 2

    order1 = Order.query.get(1)
    assert order1.courier_id == None
    assert order1.assign_time == None

    order2 = Order.query.get(2)
    assert order2.courier_id == 1

    order3 = Order.query.get(3)
    assert order3.courier_id == 1

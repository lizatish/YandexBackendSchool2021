import json

BASE_URL = 'http://0.0.0.0:8081/couriers'
METHOD = 'POST'


# def test_valid_login_logout(test_client, dbsession):
#     json = {
#         "data": [
#             {
#                 "courier_id": 123323,
#                 "courier_type": "foot",
#                 "regions": [1, 12, 22],
#                 "working_hours": ["11:35-14:05", "09:00-11:00"]
#             }
#         ]
#     }
#
#     response = test_client.post('/orders', data=json)
#     assert response.status_code == 201


def test_post_one_courier(dbsession, test_client):
    data = {
        'data':
            [
                {
                    "courier_id": 1,
                    "courier_type": "foot",
                    "regions": [1, 12, 22],
                    "working_hours": ["11:35-14:05", "09:00-11:00"]
                },
                {
                    "courier_id": 2,
                    "courier_type": "bike",
                    "regions": [22],
                    "working_hours": ["09:00-18:00"]
                }
            ]
    }

    response = test_client.post('/couriers', headers={"Content-Type": "application/json"},
                           data=json.dumps(data))
    assert response.status_code == 201
    # assert {} == response.get_json()
    #
    # courier = dbsession.query(Courier).filter_by(id=1).first()
    # assert courier is not None
    # assert courier.courier_type == 'foot'
    # assert courier.regions == [1, 12, 22]
    # assert courier.get_working_hours() == ["11:35-14:05", "09:00-11:00"]

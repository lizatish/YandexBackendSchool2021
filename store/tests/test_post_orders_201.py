# import json
#
# HEADERS = {"Content-Type": "application/json"}
# ROUTE = '/orders'
#
#
# def test_post_one_courier_post_one_courier_base_data(test_client):
#     data = {
#         "data": [
#             {
#                 "order_id": 1,
#                 "weight": 0.23,
#                 "region": 12,
#                 "delivery_hours": ["09:00-18:00"]
#             }
#         ]
#     }
#
#     response = test_client.post(ROUTE, headers=HEADERS, data=json.dumps(data))
#     assert response.status_code == 201
#
#     courier = Courier.query.get(1)
#     assert courier.courier_type == CourierType.FOOT
#     assert courier.regions == [1, 12, 22]
#     assert courier.get_working_hours() == ["11:35-14:05", "09:00-11:00"]

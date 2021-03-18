from flask import jsonify, request

from store import app, db
from store.models.courier import Courier
from store.models.order import Order


@app.route('/couriers', methods=['POST'])
def post_courier():
    couriers = request.json

    result_ids = []
    for courier in couriers['data']:
        if not Courier.query.filter_by(courier_id=courier['courier_id']).first():
            new_courier = Courier()
            new_courier.from_dict(courier)
            db.session.add(new_courier)
            db.session.commit()
            result_ids.append({'id': new_courier.courier_id})
        # else:
        #     raise ValidationError()

    response = jsonify({'couriers': result_ids})
    response.status_code = 201
    return response


@app.route('/couriers/<courier_id>', methods=['GET'])
def get_courier(courier_id):
    courier = Courier.query.get_or_404(courier_id)
    response = jsonify(courier.to_dict(addition_info=True))
    response.status_code = 200
    return response


@app.route('/couriers/<courier_id>', methods=['PATCH'])
def patch_courier(courier_id):
    data = request.json
    courier = Courier.query.get_or_404(courier_id)
    courier.from_dict(data)
    db.session.commit()

    response = jsonify(courier.to_dict())
    response.status_code = 200
    return response


@app.route('/orders', methods=['POST'])
def post_order():
    orders = request.json

    result_ids = []
    for order in orders['data']:
        if not Order.query.filter_by(order_id=order['order_id']).first():
            new_order = Order()
            new_order.from_dict(order)
            db.session.add(new_order)
            db.session.commit()
            result_ids.append({'id': new_order.order_id})
        # else:
        #     raise ValidationError()

    response = jsonify({'orders': result_ids})
    response.status_code = 201
    return response


@app.route('/orders/assign', methods=['POST'])
def post_order_assign():
    return 'helllo'


@app.route('/orders/complete', methods=['POST'])
def post_complete_assign():
    return 'helllo'

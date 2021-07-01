from store.main.models.courier import Courier
from store.main.models.order import Order


def test_session(dbsession):
    courier1 = Courier()
    courier1.courier_type = 'FOOT'
    courier1.regions = [12, 13]
    dbsession.add(courier1)

    order1 = Order()
    order1.weight = 100
    order1.region = 12
    order1.courier_id = courier1.id
    dbsession.add(order1)

    dbsession.commit()

    orders = dbsession.query(Order).filter(Order.region == 12).all()
    assert len(orders) == 1

    couriers = dbsession.query(Courier).filter(Courier.courier_type == 'FOOT').all()
    assert len(couriers) == 1

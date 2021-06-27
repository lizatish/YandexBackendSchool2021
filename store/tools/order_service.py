from store import db
from store.models.completed_order import CompletedOrders
from store.models.order import Order
from store.tools.time_service import TimeService


class OrderService:
    @staticmethod
    def add_orders(orders):
        success, errors = list(), list()
        for idx, order in enumerate(orders):

            order_id = order['order_id']
            temp_courier = Order.query.get(order_id)

            if not temp_courier:
                new_order = Order()
                new_order.from_dict(order)
                db.session.add(new_order)
                success.append(order_id)
            else:
                errors.append(order_id)
        if not errors:
            db.session.commit()
        return success, errors

    @staticmethod
    def get_order(id):
        order = Order.query.get(id)
        return order

    @staticmethod
    def release_orders(orders):
        for order in orders:
            order.courier_id = None
            order.assign_time = None
        db.session.commit()

    @staticmethod
    def refresh_assign_time(courier):
        orders = Order.query.filter(
            Order.courier_id == courier.id,
            Order.is_complete == False
        ).all()

        if orders:
            assign_time = TimeService.get_assign_time()

            for order in orders:
                order.assign_time = assign_time
            db.session.commit()

        return orders

    @staticmethod
    def complete_order(order, complete_time):
        from store.tools.courier_service import CourierService

        order.is_complete = True
        order.complete_time = complete_time
        courier = CourierService.get_courier(order.courier_id)
        courier.current_weight -= order.weight
        db.session.commit()

        complete_order = CompletedOrders.query.filter(
            CompletedOrders.courier_id == order.courier_id,
            CompletedOrders.region == order.region
        ).first()
        if not complete_order:
            complete_order = CompletedOrders(
                courier_id=order.courier_id,
                completed_orders=1,
                last_complete_time=order.complete_time,
                general_complete_seconds=(order.complete_time - order.assign_time).total_seconds(),
                region=order.region
            )
            db.session.add(complete_order)
        else:
            total_secs = (order.complete_time - complete_order.last_complete_time).total_seconds()
            complete_order.completed_orders += 1
            complete_order.last_complete_time = order.complete_time
            complete_order.general_complete_seconds += total_secs

        db.session.commit()

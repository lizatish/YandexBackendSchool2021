from store import db
from store.models.courier import Courier
from store.tools.order_service import OrderService
from store.tools.time_service import TimeService


class CourierService:
    @staticmethod
    def add_couriers(couriers):
        success, errors = list(), list()
        for idx, courier in enumerate(couriers):

            courier_id = courier['courier_id']
            temp_courier = Courier.query.get(courier_id)

            if not temp_courier:
                new_courier = Courier()
                new_courier.from_dict(courier)
                db.session.add(new_courier)
                success.append(courier_id)
            else:
                errors.append(courier_id)
        if not errors:
            db.session.commit()
        return success, errors

    @staticmethod
    def get_courier(id):
        courier = Courier.query.get(id)
        return courier

    @staticmethod
    def edit_courier(courier, data):
        courier.edit(data)
        intersection_orders = CourierService.get_intersection_orders(courier)
        OrderService.release_orders(intersection_orders)

    @staticmethod
    def get_intersection_orders(courier):
        return courier.check_time_not_intersection()

    @staticmethod
    def get_assign_orders(courier):
        orders = courier.balancer_orders()
        time_service = TimeService()
        for order in orders:
            order.assign_time = time_service.get_assign_time()
        db.session.commit()
        return orders

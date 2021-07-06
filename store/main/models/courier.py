from math import inf
from typing import List

from store import db
from store.main.models.completed_order import CompletedOrders
from store.main.models.courier_assign_time import CourierAssignTime
from store.main.models.courier_type import CourierType
from store.main.models.order import Order
from store.main.models.order_assign_time import OrderAssignTime


class Courier(db.Model):
    __tablename__ = 'courier'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    courier_type = db.Column(db.Enum(CourierType))
    regions = db.Column(db.ARRAY(db.Integer))

    current_weight = db.Column(db.Float, default=0.0)
    max_weight = db.Column(db.Integer)

    orders: List[Order] = db.relationship(Order, backref=db.backref('courier'))
    completed_orders: List[CompletedOrders] = db.relationship(CompletedOrders, backref=db.backref('courier'))
    assign_times: List[CourierAssignTime] = db.relationship(CourierAssignTime, backref=db.backref('courier'))

    def get_weight(self):
        return float(self.current_weight)

    def from_dict(self, data):
        for field in ['courier_id', 'courier_type', 'regions', 'working_hours']:
            if field in data:
                if field == 'courier_type':
                    self.courier_type = CourierType.get_type(data[field])
                    self.max_weight = CourierType.get_max_weight(self.courier_type)
                elif field == 'working_hours':
                    for working_hour in data[field]:
                        assign_time = CourierAssignTime(working_hour, data['courier_id'])
                        db.session.add(assign_time)
                elif field == 'courier_id':
                    setattr(self, 'id', data[field])
                else:
                    setattr(self, field, data[field])

    def lose_weight(self, val):
        self.current_weight -= val

    def to_dict(self):
        json_data = {
            'courier_id': self.id,
            'courier_type': self.courier_type.value,
            'regions': self.regions,
            'working_hours': self.get_working_hours(),
        }
        if self.completed_orders:
            json_data['rating'] = self.calculate_rating()
        json_data['earnings'] = self.calculate_earnings()
        return json_data

    def edit(self, data):
        for field in data:
            if field == 'courier_type':
                self.courier_type = CourierType.get_type(data[field])
                self.max_weight = CourierType.get_max_weight(self.courier_type)
            elif field == 'working_hours':
                for old_assign_time in self.assign_times:
                    db.session.delete(old_assign_time)

                for working_hour in data[field]:
                    assign_time = CourierAssignTime(working_hour, self.id)
                    db.session.add(assign_time)

            else:
                setattr(self, field, data[field])

    def get_working_hours(self):
        return [str(assign_time) for assign_time in self.assign_times]

    # TODO разбить на функции
    def balancer_orders(self):
        orders = Order.query.filter(
            Order.courier_id == None,
            Order.is_complete == False,
            Order.weight + self.current_weight <= self.max_weight,
            Order.region.in_(self.regions)
        ).order_by(Order.weight).all()

        new_orders = []
        for order in orders:
            order_assign_times = OrderAssignTime.query.filter_by(
                order_id=order.id
            ).order_by(OrderAssignTime.time_start_hour, OrderAssignTime.time_start_min,
                       OrderAssignTime.time_finish_hour, OrderAssignTime.time_finish_min).all()

            courier_assign_times = CourierAssignTime.query.filter(
                CourierAssignTime.courier_id == self.id).all()

            for courier_time in courier_assign_times:
                for order_time in order_assign_times:
                    if self.current_weight + order.weight <= self.max_weight:

                        if courier_time.time_start_hour >= order_time.time_finish_hour or \
                                order_time.time_start_hour >= courier_time.time_finish_hour:
                            continue

                        order.courier_id = self.id
                        new_orders.append(order)
                        self.current_weight += order.weight
                        break
                    else:
                        break
                if self.current_weight + order.weight == self.max_weight or \
                        order.courier_id:
                    break
        return new_orders

    def get_active_orders(self):
        return Order.query.filter_by(courier_id=self.id, is_complete=False).all()

    # TODO написать тесты на баланс распределения заказов на курьера (все должно работать, но нужны тесты)
    def check_intersection_with_orders(self):
        active_orders = set(self.get_active_orders())
        intersect_orders = set()

        intersect_orders |= self.check_intersection_by_regions(active_orders)
        active_orders -= intersect_orders

        if self.current_weight <= self.max_weight:
            return intersect_orders

        intersect_orders |= self.check_intersection_by_working_hours(active_orders)
        active_orders -= intersect_orders

        if self.current_weight <= self.max_weight:
            return intersect_orders.union(intersect_orders)

        intersect_orders |= self.check_weight_intersection(active_orders)
        return intersect_orders

    def check_weight_intersection(self, active_orders):
        intersect_orders = set()
        for order in active_orders:
            if self.current_weight >= self.max_weight:
                self.current_weight -= order.weight
                intersect_orders.add(order)
        return intersect_orders

    def check_intersection_by_regions(self, active_orders):
        intersect_orders = set()
        for order in active_orders:
            if order.region not in self.regions:
                intersect_orders.add(order)
                self.current_weight -= order.weight
        return intersect_orders

    def check_intersection_by_working_hours(self, active_orders):
        intersect_orders = set()
        courier_assign_times = self.get_assign_times()
        for order in active_orders:
            order_assign_times = order.get_assign_times()
            for courier_time in courier_assign_times:
                for order_time in order_assign_times:
                    if courier_time.time_start_hour >= order_time.time_finish_hour or \
                            order_time.time_start_hour >= courier_time.time_finish_hour:
                        self.current_weight -= order.weight
                        intersect_orders.add(order)
                        break
        return intersect_orders

    def get_assign_times(self):
        return CourierAssignTime.query.filter_by(courier_id=self.id).all()

    def calculate_rating(self):
        t = inf
        for order in self.completed_orders:
            average_t = order.general_complete_seconds / order.completed_orders
            t = min(t, average_t)
        rating = (60 * 60 - min(t, 60 * 60)) / (60 * 60) * 5
        return float(f"{rating:.2f}")

    def calculate_earnings(self):
        sum_orders = 0
        if not self.completed_orders:
            return sum_orders

        for order in self.completed_orders:
            sum_orders += 500 * order.completed_orders * CourierType.get_coefficient(self.courier_type)
        return sum_orders

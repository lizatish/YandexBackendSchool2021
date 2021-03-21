from typing import List

from store import db
from store.models.completed_order import CompletedOrder
from store.models.courier_assign_time import CourierAssignTime
from store.models.courier_type import CourierType
from store.models.order import Order
from store.models.order_assign_time import OrderAssignTime


class Courier(db.Model):
    courier_id = db.Column(db.Integer, primary_key=True, unique=True)
    courier_type = db.Column(db.Enum(CourierType))
    regions = db.Column(db.ARRAY(db.Integer))
    rating = db.Column(db.Integer, default=0)
    earnings = db.Column(db.Integer, default=0)

    current_weight = db.Column(db.Integer, default=0)
    max_weight = db.Column(db.Integer)

    orders: List[Order] = db.relationship(Order, backref=db.backref('courier'))
    completed_orders: List[CompletedOrder] = db.relationship(CompletedOrder, backref=db.backref('courier'))

    assign_times: List[CourierAssignTime] = db.relationship(CourierAssignTime, backref=db.backref('courier'))

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
                else:
                    setattr(self, field, data[field])

    def edit(self, data):
        for field in ['courier_type', 'regions', 'working_hours']:
            if field in data:
                if field == 'courier_type':
                    self.courier_type = CourierType.get_type(data[field])
                    self.max_weight = CourierType.get_max_weight(self.courier_type)
                elif field == 'working_hours':
                    for working_hour in data[field]:
                        for old_assign_time in self.assign_times:
                            db.session.delete(old_assign_time)
                        assign_time = CourierAssignTime(working_hour, self.courier_id)
                        db.session.add(assign_time)
                else:
                    setattr(self, field, data[field])

    def to_dict(self, addition_info=False):
        data = {
            'courier_id': self.courier_id,
            'courier_type': self.courier_type.value,
            'regions': self.regions,
            'working_hours': self.get_working_hours(),
        }
        if addition_info:
            data['rating'] = self.rating
            data['earnings'] = self.earnings
        return data

    def get_working_hours(self):
        return [str(assign_time) for assign_time in self.assign_times]

    def balancer_orders(self):
        orders = Order.query.filter(
            Order.courier_id == None,
            Order.is_complete == False,
            Order.region.in_(self.regions)
        ).all()

        for order in orders:
            order_assign_times = OrderAssignTime.query.filter(
                OrderAssignTime.order_id == order.order_id
            ).order_by(OrderAssignTime.time_start_hour, OrderAssignTime.time_start_min,
                       OrderAssignTime.time_finish_hour, OrderAssignTime.time_finish_min).all()

            courier_assign_times = CourierAssignTime.query.filter(
                CourierAssignTime.courier_id == self.courier_id).all()

            for courier_time in courier_assign_times:
                for order_time in order_assign_times:
                    if self.current_weight + order.weight <= self.max_weight:

                        if courier_time.time_start_hour >= order_time.time_finish_hour:
                            continue
                        elif order_time.time_start_hour >= courier_time.time_finish_hour:
                            continue

                        order.courier_id = self.courier_id
                        break
                    else:
                        break
                if self.current_weight + order.weight == self.max_weight or \
                        order.courier_id:
                    break

    def check_time_not_intersection(self):

        not_intersections = []

        orders = Order.query.filter(
            Order.courier_id == self.courier_id,
            Order.is_complete == False
        ).all()

        for order in orders:
            order_assign_times = OrderAssignTime.query.filter(
                OrderAssignTime.order_id == order.order_id
            ).order_by(OrderAssignTime.time_start_hour, OrderAssignTime.time_start_min,
                       OrderAssignTime.time_finish_hour, OrderAssignTime.time_finish_min).all()

            courier_assign_times = CourierAssignTime.query.filter(
                CourierAssignTime.courier_id == self.courier_id).all()

            for courier_time in courier_assign_times:
                for order_time in order_assign_times:
                    if self.current_weight + order.weight >= self.max_weight:
                        not_intersections.append(order)
                        break

                    if courier_time.time_start_hour >= order_time.time_finish_hour:
                        not_intersections.append(order)
                        break
                    elif order_time.time_start_hour >= courier_time.time_finish_hour:
                        not_intersections.append(order)
                        break
                if order in not_intersections:
                    break

        return not_intersections

    def calculate_rating(self):
        Order.query.filter(
            Order.courier_id == self.courier_id,
            Order.is_complete == True
        ).all()

        t = None
        self.rating = (60 * 60 - min(t, 60 * 60)) / (60 * 60) * 5

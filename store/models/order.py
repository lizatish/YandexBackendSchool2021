from typing import List

from store import db
from store.models.order_assign_time import OrderAssignTime


class Order(db.Model):
    __tablename__ = 'order'

    order_id = db.Column(db.Integer, primary_key=True, unique=True)
    courier_id = db.Column(db.Integer, db.ForeignKey('courier.courier_id'))

    weight = db.Column(db.DECIMAL)
    region = db.Column(db.Integer)

    is_complete = db.Column(db.Boolean, default=False)
    complete_time = db.Column(db.DateTime)
    assign_time = db.Column(db.DateTime)

    assign_times: List[OrderAssignTime] = db.relationship(OrderAssignTime, backref=db.backref('order'))

    def from_dict(self, data):
        for field in ['order_id', 'weight', 'region', 'delivery_hours']:
            if field in data:
                if field == 'delivery_hours':
                    for working_hour in data[field]:
                        assign_time = OrderAssignTime(working_hour, data['order_id'])
                        db.session.add(assign_time)
                else:
                    setattr(self, field, data[field])

    def to_dict(self):
        data = {
            'order_id': self.order_id,
            'weight': self.weight,
            'region': self.region,
            'working_hours': self.get_working_hours()
        }
        return data

    def get_working_hours(self):
        return [str(assign_time) for assign_time in self.assign_times]

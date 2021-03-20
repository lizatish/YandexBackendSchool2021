from typing import List

from store import db
from store.models.courier_assign_time import CourierAssignTime
from store.models.courier_type import CourierType
from store.models.order import Order


class Courier(db.Model):
    courier_id = db.Column(db.Integer, primary_key=True, unique=True)
    courier_type = db.Column(db.Enum(CourierType))
    regions = db.Column(db.ARRAY(db.Integer))
    rating = db.Column(db.Integer, default=0)
    earnings = db.Column(db.Integer, default=0)

    current_weight = db.Column(db.Integer, default=0)
    max_weight = db.Column(db.Integer)

    orders = db.relationship(Order, backref=db.backref('courier'))
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

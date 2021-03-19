from store import db
from store.models.courier_assign_time import CourierAssignTime
from store.models.courier_type import CourierType
from store.models.order import Order


class Courier(db.Model):
    courier_id = db.Column(db.Integer, primary_key=True, unique=True)
    courier_type = db.Column(db.Enum(CourierType))
    regions = db.Column(db.ARRAY(db.Integer))
    # working_hours = db.Column(db.ARRAY(db.String(30)))
    rating = db.Column(db.Integer)
    earnings = db.Column(db.Integer)

    orders = db.relationship(Order, backref=db.backref('courier'))
    assign_times = db.relationship(CourierAssignTime, backref=db.backref('courier'))

    def from_dict(self, data):
        for field in ['courier_id', 'courier_type', 'regions']:
            if field in data:
                if field == 'courier_type':
                    self.courier_type = CourierType.get_type(data[field])
                else:
                    setattr(self, field, data[field])

    def to_dict(self, addition_info=False):
        data = {
            'courier_id': self.courier_id,
            'courier_type': self.courier_type,
            'regions': self.regions,
            'working_hours': self.working_hours,
        }
        if addition_info:
            data['rating'] = self.rating
            data['earnings'] = self.earnings
        return data

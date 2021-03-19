from store import db
from store.models.serializator import JsonMixin


class Order(db.Model, JsonMixin):
    order_id = db.Column(db.Integer, primary_key=True)
    weight = db.Column(db.Integer)
    region = db.Column(db.Integer)
    # delivery_hours = db.Column(db.ARRAY(db.String))

    courier_id = db.Column(db.Integer, db.ForeignKey('courier.courier_id'))

    is_complete = db.Column(db.Boolean, default=False)

    time_start_hour = db.Column(db.Integer)
    time_start_min = db.Column(db.Integer)
    time_finish_hour = db.Column(db.Integer)
    time_finish_min = db.Column(db.Integer)

    def from_dict(self, data):
        for field in ['order_id', 'weight', 'region', 'delivery_hours']:
            if field in data:
                if field == 'delivery_hours':
                    self.set_delivery_hours(data[field])
                else:
                    setattr(self, field, data[field])

    def set_delivery_hours(self, delivery_hours):
        data = delivery_hours.split('-')
        self.time_start_hour, self.time_start_min = [int(k) for k in data[0].split(':')]
        self.time_start_hour, self.time_start_min = [int(k) for k in data[1].split(':')]

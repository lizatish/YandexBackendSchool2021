from store import db
from store.models.serializator import JsonMixin


class Order(db.Model, JsonMixin):
    order_id = db.Column(db.Integer, primary_key=True)
    weight = db.Column(db.Integer)
    region = db.Column(db.Integer)
    delivery_hours = db.Column(db.ARRAY(db.String))

    courier_id = db.Column(db.Integer, db.ForeignKey('courier.courier_id'))

    is_complete = db.Column(db.Boolean, default=False)
    is_assign = db.Column(db.Boolean, default=False)


    def from_dict(self, data):
        for field in ['order_id', 'weight', 'regions', 'delivery_hours']:
            if field in data:
                setattr(self, field, data[field])

from store import db
from store.models.serializator import JsonMixin


class Courier(db.Model, JsonMixin):
    courier_id = db.Column(db.Integer, primary_key=True)
    courier_type = db.Column(db.String(30))
    regions = db.Column(db.ARRAY(db.Integer))
    working_hours = db.Column(db.ARRAY(db.String(30)))
    rating = db.Column(db.Integer)
    earnings = db.Column(db.Integer)

    def from_dict(self, data):
        for field in ['courier_id', 'courier_type', 'regions', 'working_hours']:
            if field in data:
                setattr(self, field, data[field])

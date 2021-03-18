from store import db
from store.models.serializator import JsonMixin


class Order(db.Model, JsonMixin):
    id = db.Column(db.Integer, primary_key=True)
    weight = db.Column(db.Integer)
    region = db.Column(db.Integer)
    delivery_hours = db.Column(db.ARRAY(db.String))
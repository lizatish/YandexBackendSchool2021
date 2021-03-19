from store import db
from store.models.serializator import JsonMixin


class CourierAssignTime(db.Model, JsonMixin):
    courier_id = db.Column(db.Integer, db.ForeignKey('courier.courier_id'))

    id = db.Column(db.Integer, primary_key=True)
    time_start_hour = db.Column(db.Integer)
    time_start_min = db.Column(db.Integer)
    time_finish_hour = db.Column(db.Integer)
    time_finish_min = db.Column(db.Integer)

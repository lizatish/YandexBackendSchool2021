from store import db
from store.models.serializator import JsonMixin


class AssignTime(db.Model, JsonMixin):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(30))
    example = db.Column(db.String(50))

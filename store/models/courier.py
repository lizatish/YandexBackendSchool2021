from store import db


class Courier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(30))
    regions = db.Column(db.ARRAY(db.Integer))
    working_hours = db.Column(db.ARRAY(db.String(30)))
    rating = db.Column(db.Integer)
    earnings = db.Column(db.Integer)

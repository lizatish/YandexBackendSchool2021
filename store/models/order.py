from store import db


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)

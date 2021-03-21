from store import db


class CompletedOrder(db.Model):
    id =  db.Column(db.Integer, primary_key=True)
    courier_id = db.Column(db.Integer, db.ForeignKey('courier.courier_id'))
    completed_orders = db.Column(db.Integer, default=0)
    min_time = db.Column(db.Integer)

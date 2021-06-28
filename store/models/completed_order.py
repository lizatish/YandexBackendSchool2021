from store import db


class CompletedOrders(db.Model):
    __tablename__ = 'completed_orders'

    id = db.Column(db.Integer, primary_key=True)
    courier_id = db.Column(db.Integer, db.ForeignKey('courier.id'))
    completed_orders = db.Column(db.Integer, default=0)
    last_complete_time = db.Column(db.DateTime)
    general_complete_seconds = db.Column(db.DECIMAL)
    region = db.Column(db.Integer)

    def update(self, order):
        total_secs = (order.complete_time - self.last_complete_time).total_seconds()
        self.completed_orders += 1
        self.last_complete_time = order.complete_time
        self.general_complete_seconds += total_secs

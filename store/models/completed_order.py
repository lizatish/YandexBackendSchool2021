from store import db
from store.models import Base


class CompletedOrders(Base):
    __tablename__ = 'completed_orders'

    id = db.Column(db.Integer, primary_key=True)
    courier_id = db.Column(db.Integer, db.ForeignKey('courier.courier_id'))
    completed_orders = db.Column(db.Integer, default=0)
    last_complete_time = db.Column(db.DateTime)
    general_complete_seconds = db.Column(db.DECIMAL)
    region = db.Column(db.Integer)

from store import db


class OrderAssignTime(db.Model):
    __tablename__ = 'order_assign_time'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))

    time_start_hour = db.Column(db.Integer)
    time_start_min = db.Column(db.Integer)
    time_finish_hour = db.Column(db.Integer)
    time_finish_min = db.Column(db.Integer)

    def __init__(self, delivery_hours, order_id):
        data = delivery_hours.split('-')
        time_start_hour, time_start_min = [int(k) for k in data[0].split(':')]
        time_finish_hour, time_finish_min = [int(k) for k in data[1].split(':')]
        self.order_id = order_id
        self.time_start_hour = time_start_hour
        self.time_start_min = time_start_min
        self.time_finish_hour = time_finish_hour
        self.time_finish_min = time_finish_min

    def __str__(self):
        return f'{str(self.time_start_hour).rjust(2, "0")}:{str(self.time_start_min).rjust(2, "0")}-' \
               f'{str(self.time_finish_hour).rjust(2, "0")}:{str(self.time_finish_min).rjust(2, "0")}'

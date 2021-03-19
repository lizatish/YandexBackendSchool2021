from store import db


class Order(db.Model):
    order_id = db.Column(db.Integer, primary_key=True)
    courier_id = db.Column(db.Integer, db.ForeignKey('courier.courier_id'))

    weight = db.Column(db.Integer)
    region = db.Column(db.Integer)

    time_start_hour = db.Column(db.Integer)
    time_start_min = db.Column(db.Integer)
    time_finish_hour = db.Column(db.Integer)
    time_finish_min = db.Column(db.Integer)

    is_complete = db.Column(db.Boolean, default=False)
    complete_time = db.Column(db.DateTime)

    def from_dict(self, data):
        for field in ['order_id', 'weight', 'region', 'delivery_hours']:
            if field in data:
                if field == 'delivery_hours':
                    for working_hour in data[field]:
                        self.set_delivery_hours(working_hour)
                else:
                    setattr(self, field, data[field])

    def set_delivery_hours(self, delivery_hours):
        data = delivery_hours.split('-')
        self.time_start_hour, self.time_start_min = [int(k) for k in data[0].split(':')]
        self.time_finish_hour, self.time_finish_min = [int(k) for k in data[1].split(':')]

    def to_dict(self):
        data = {
            'order_id': self.order_id,
            'weight': self.weight,
            'region': self.region,
            'working_hours': self.get_working_hours()
        }
        return data

    def get_working_hours(self):
        return f'{str(self.time_start_hour).rjust(2, "0")}:{str(self.time_start_min).rjust(2, "0")}-' \
               f'{str(self.time_finish_hour).rjust(2, "0")}:{str(self.time_finish_min).rjust(2, "0")}'

from store import db
from store.models.serializator import JsonMixin


class CourierAssignTime(db.Model, JsonMixin):
    courier_id = db.Column(db.Integer, db.ForeignKey('courier.courier_id'))

    id = db.Column(db.Integer, primary_key=True)
    time_start_hour = db.Column(db.Integer)
    time_start_min = db.Column(db.Integer)
    time_finish_hour = db.Column(db.Integer)
    time_finish_min = db.Column(db.Integer)

    def __init__(self, delivery_hours, courier_id):
        data = delivery_hours.split('-')
        time_start_hour, time_start_min = [int(k) for k in data[0].split(':')]
        time_finish_hour, time_finish_min = [int(k) for k in data[1].split(':')]
        self.courier_id = courier_id
        self.time_start_hour = time_start_hour
        self.time_start_min = time_start_min
        self.time_finish_hour = time_finish_hour
        self.time_finish_min = time_finish_min



    @staticmethod
    def get_assign_time(delivery_hours, courier_id):
        assign_times = []

        for hours in delivery_hours:
            data = hours.split('-')
            time_start_hour, time_start_min = [int(k) for k in data[0].split(':')]
            time_finish_hour, time_finish_min = [int(k) for k in data[1].split(':')]
            assign_time = CourierAssignTime(courier_id=courier_id,
                                            time_start_hour=time_start_hour,
                                            time_start_min=time_start_min,
                                            time_finish_hour=time_finish_hour,
                                            time_finish_min=time_finish_min)
            assign_times.append(assign_time)
        return assign_times

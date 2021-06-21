from sqlalchemy import Integer, Column

from store import db
from store.models import Base


class CourierAssignTime(Base):
    __tablename__ = 'courier_assign_time'

    id = db.Column(Integer, primary_key=True)
    time_start_hour = Column(Integer)
    time_start_min = Column(Integer)
    time_finish_hour = Column(Integer)
    time_finish_min = Column(Integer)

    courier_id = db.Column(db.Integer, db.ForeignKey('courier.courier_id'))

    def __init__(self, delivery_hours, courier_id):
        data = delivery_hours.split('-')
        time_start_hour, time_start_min = [int(k) for k in data[0].split(':')]
        time_finish_hour, time_finish_min = [int(k) for k in data[1].split(':')]
        self.courier_id = courier_id
        self.time_start_hour = time_start_hour
        self.time_start_min = time_start_min
        self.time_finish_hour = time_finish_hour
        self.time_finish_min = time_finish_min

    def __str__(self):
        return f'{str(self.time_start_hour).rjust(2, "0")}:{str(self.time_start_min).rjust(2, "0")}-' \
               f'{str(self.time_finish_hour).rjust(2, "0")}:{str(self.time_finish_min).rjust(2, "0")}'

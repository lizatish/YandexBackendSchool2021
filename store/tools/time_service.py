from datetime import datetime


class TimeService:
    @staticmethod
    def get_assign_time():
        return datetime.utcnow().strftime('%Y-%m-%dT%-H:%M:%S.%f'[:-3] + 'Z')

    @staticmethod
    def get_assign_time_from_datetime(dt):
        return dt.strftime('%Y-%m-%dT%-H:%M:%S.%f'[:-3] + 'Z')
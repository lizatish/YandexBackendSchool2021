import enum


class CourierType(enum.Enum):
    FOOT = 10
    BIKE = 15
    CAR = 50

    @classmethod
    def get_type(cls, type):
        if type == 'foot':
            return CourierType.FOOT
        elif type == 'bike':
            return CourierType.BIKE
        elif type == 'car':
            return CourierType.CAR


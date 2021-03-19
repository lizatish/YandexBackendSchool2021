import enum


class CourierType(enum.Enum):
    FOOT = "foot"
    BIKE = "bike"
    CAR = "car"

    @classmethod
    def get_type(cls, type):
        if type == 'foot':
            return CourierType.FOOT
        elif type == 'bike':
            return CourierType.BIKE
        elif type == 'car':
            return CourierType.CAR

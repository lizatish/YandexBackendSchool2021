import enum


class CourierType(enum.Enum):
    FOOT = "foot"
    BIKE = "bike"
    CAR = "car"

    @staticmethod
    def get_type(type):
        if type == 'foot':
            return CourierType.FOOT
        elif type == 'bike':
            return CourierType.BIKE
        elif type == 'car':
            return CourierType.CAR

    @staticmethod
    def max_weight(type):
        if type == CourierType.FOOT:
            return 10
        elif type == CourierType.BIKE:
            return 15
        elif type == CourierType.CAR:
            return 50

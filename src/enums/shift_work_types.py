from enum import StrEnum, auto

__all__ = ('ShiftWorkType',)


class ShiftWorkType(StrEnum):
    MOVE_TO_WASH = auto()
    LIGHT_WASHES = auto()
    FIND_VEHICLE_IN_CITY = auto()
    ASSIGNMENT_MOVE = auto()

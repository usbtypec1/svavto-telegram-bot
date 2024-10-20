from enum import StrEnum, auto

__all__ = ('CarClass',)


class CarClass(StrEnum):
    COMFORT = auto()
    BUSINESS = auto()
    VAN = auto()

from enum import StrEnum, auto

__all__ = ('CallbackDataPrefix',)


class CallbackDataPrefix(StrEnum):
    PERFORMER_REGISTER = auto()
    CAR_WASH_DETAIL = auto()
    CAR_WASH_CREATE = auto()
    CAR_WASH_LIST = auto()
    CAR_WASH_CREATE_CONFIRM = auto()
    STAFF_DETAIL = auto()
    STAFF_UPDATE = auto()

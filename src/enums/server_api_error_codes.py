from enum import StrEnum, auto

__all__ = ('ServerApiErrorCode',)


class ServerApiErrorCode(StrEnum):
    STAFF_NOT_FOUND = auto()
    STAFF_ALREADY_EXISTS = auto()
    STAFF_HAS_NO_ACTIVE_SHIFT = auto()
    CAR_WASH_SAME_AS_CURRENT = auto()
    CAR_WASH_NOT_FOUND = auto()
    SHIFT_FOR_SPECIFIC_DATE_NOT_FOUND = auto()
    SHIFT_NOT_CONFIRMED = auto()
    STAFF_HAS_ACTIVE_SHIFT = auto()
    SHIFT_ALREADY_FINISHED = auto()
    SHIFT_ALREADY_CONFIRMED = auto()
    STAFF_HAS_NO_ANY_SHIFT = auto()
    SHIFT_NOT_FOUND = auto()
    CAR_ALREADY_WASHED_ON_SHIFT = auto()
    SHIFT_ALREADY_EXISTS = auto()
    ADDITIONAL_SERVICE_COULD_NOT_BE_PROVIDED = auto()
    STAFF_REGISTER_REQUEST_ALREADY_EXISTS = auto()
    INVALID_TIME_TO_START_SHIFT = auto()

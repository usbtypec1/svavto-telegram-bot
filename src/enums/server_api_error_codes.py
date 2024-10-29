from enum import StrEnum, auto

__all__ = ('ServerApiErrorCode',)


class ServerApiErrorCode(StrEnum):
    STAFF_NOT_FOUND = auto()
    STAFF_ALREADY_EXISTS = auto()
    STAFF_HAS_NO_ACTIVE_SHIFT = auto()

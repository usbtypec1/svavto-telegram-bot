from enum import StrEnum, auto

__all__ = ('ServerApiErrorCode',)


class ServerApiErrorCode(StrEnum):
    STAFF_NOT_FOUND = auto()

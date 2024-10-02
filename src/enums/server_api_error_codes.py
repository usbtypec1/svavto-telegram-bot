from enum import StrEnum, auto

__all__ = ('ServerApiErrorCode',)


class ServerApiErrorCode(StrEnum):
    PERFORMER_NOT_FOUND = auto()

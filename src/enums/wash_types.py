from enum import StrEnum, auto

__all__ = ('WashType',)


class WashType(StrEnum):
    PLANNED = auto()
    URGENT = auto()

from enum import StrEnum, auto

__all__ = ('PenaltyReason',)


class PenaltyReason(StrEnum):
    NOT_SHOWING_UP = auto()
    EARLY_LEAVE = auto()
    LATE_REPORT = auto()

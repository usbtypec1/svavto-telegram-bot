from enum import StrEnum, auto

__all__ = ('PenaltyConsequence',)


class PenaltyConsequence(StrEnum):
    DISMISSAL = auto()
    WARN = auto()

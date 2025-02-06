from enum import auto, StrEnum

__all__ = ('ShiftType',)


class ShiftType(StrEnum):
    REGULAR = auto()
    EXTRA = auto()
    TEST = auto()

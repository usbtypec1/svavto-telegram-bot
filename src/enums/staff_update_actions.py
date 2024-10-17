from enum import StrEnum, auto

__all__ = ('StaffUpdateAction',)


class StaffUpdateAction(StrEnum):
    BAN = auto()
    UNBAN = auto()

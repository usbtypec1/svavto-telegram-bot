from enum import StrEnum, auto

__all__ = ('StaffUpdateAction',)


class StaffUpdateAction(StrEnum):
    BAN = auto()
    UNBAN = auto()
    TO_CAR_TRANSPORTER = auto()
    TO_CAR_TRANSPORTER_AND_WASHER = auto()

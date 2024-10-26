from enum import StrEnum, auto

__all__ = ('MailingType',)


class MailingType(StrEnum):
    ALL = auto()
    SPECIFIC_STAFF = auto()
    LAST_ACTIVE = auto()

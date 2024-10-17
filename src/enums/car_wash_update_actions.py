from enum import StrEnum, auto

__all__ = ('CarWashAction',)


class CarWashAction(StrEnum):
    RENAME = auto()
    DELETE = auto()

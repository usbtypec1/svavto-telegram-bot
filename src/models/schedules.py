from pydantic import BaseModel

__all__ = ('MonthAndYear', 'StaffAvailableDates')


class MonthAndYear(BaseModel):
    month: int
    year: int


class StaffAvailableDates(BaseModel):
    staff_id: int
    dates: list[MonthAndYear]

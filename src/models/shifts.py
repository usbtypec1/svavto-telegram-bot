import datetime

from pydantic import BaseModel

from models.car_washes import CarWash

__all__ = (
    'ShiftFinishResult',
    'ShiftConfirmation',
    'Shift',
    'ShiftCreateResult',
)


class ShiftFinishResult(BaseModel):
    is_first_shift: bool
    staff_full_name: str
    car_numbers: list[str]


class ShiftConfirmation(BaseModel):
    shift_id: int
    staff_id: int
    staff_full_name: str


class Shift(BaseModel):
    id: int
    date: datetime.date
    confirmed_at: datetime.datetime | None
    started_at: datetime.datetime | None
    finished_at: datetime.datetime | None
    created_at: datetime.datetime
    car_wash: CarWash | None


class ShiftCreateResult(BaseModel):
    staff_id: int
    staff_full_name: str
    dates: list[datetime.date]

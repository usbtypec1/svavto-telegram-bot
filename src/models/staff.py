from datetime import datetime

from pydantic import BaseModel

from models import MonthAndYear

__all__ = (
    'Staff',
    'StaffToRegister',
    'StaffToRegisterWithId',
    'StaffWithAvailableDates',
)


class StaffToRegister(BaseModel):
    full_name: str
    car_sharing_phone_number: str
    console_phone_number: str


class StaffToRegisterWithId(StaffToRegister):
    id: int


class Staff(BaseModel):
    id: int
    full_name: str
    car_sharing_phone_number: str
    console_phone_number: str
    is_banned: bool
    created_at: datetime


class StaffWithAvailableDates(Staff):
    available_dates: list[MonthAndYear]

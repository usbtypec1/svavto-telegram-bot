from datetime import datetime

from pydantic import BaseModel

__all__ = ('Staff', 'StaffToCreate')


class Staff(BaseModel):
    id: int
    full_name: str
    car_sharing_phone_number: str
    console_phone_number: str
    is_banned: bool
    created_at: datetime


class StaffToCreate(BaseModel):
    id: int
    full_name: str
    car_sharing_phone_number: str
    console_phone_number: str

from datetime import datetime

from pydantic import BaseModel

__all__ = ('Staff', 'StaffToRegister')


class StaffToRegister(BaseModel):
    full_name: str
    car_sharing_phone_number: str
    console_phone_number: str


class Staff(BaseModel):
    id: int
    full_name: str
    car_sharing_phone_number: str
    console_phone_number: str
    is_banned: bool
    created_at: datetime

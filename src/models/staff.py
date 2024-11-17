from datetime import datetime

from pydantic import BaseModel

__all__ = (
    'Staff',
    'StaffToRegister',
    'StaffToRegisterWithId',
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
    banned_at: datetime | None
    created_at: datetime
    last_activity_at: datetime

    @property
    def is_banned(self) -> bool:
        return self.banned_at is not None

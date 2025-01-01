from datetime import datetime

from pydantic import BaseModel

__all__ = (
    'Staff',
    'StaffToRegister',
    'StaffToRegisterWithId',
    'StaffListPage',
    'Pagination',
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


class Pagination(BaseModel):
    limit: int
    offset: int
    total_count: int

    @property
    def is_last_page(self) -> bool:
        return self.offset + self.limit >= self.total_count

    @property
    def is_first_page(self) -> bool:
        return self.offset == 0

    @property
    def previous_offset(self) -> int:
        return self.offset - self.limit if self.offset > 0 else 0

    @property
    def next_offset(self) -> int:
        return self.offset + self.limit


class StaffListPage(BaseModel):
    staff: list[Staff]
    pagination: Pagination

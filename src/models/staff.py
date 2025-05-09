from datetime import datetime

from pydantic import BaseModel

from enums import StaffType


__all__ = (
    'Staff',
    'StaffIdAndName',
    'StaffRegisterRequestData',
    'StaffListPage',
    'Pagination',
    'StaffRegisterRequest',
    'StaffDetail',
)


class StaffIdAndName(BaseModel):
    id: int
    full_name: str


class StaffRegisterRequestData(BaseModel):
    full_name: str
    car_sharing_phone_number: str
    console_phone_number: str
    staff_type: int


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


# Есть проблема с валидацией типа когда используется @inject.
# Поэтому наследуемся от Staff
# Желательно потом разграничить эти два класса
class StaffDetail(Staff):
    type: StaffType


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

    @property
    def page_number(self) -> int:
        return self.offset // self.limit + 1

    @property
    def next_page_number(self) -> int:
        return self.page_number + 1

    @property
    def previous_page_number(self) -> int:
        return self.page_number - 1


class StaffListPage(BaseModel):
    staff: list[Staff]
    pagination: Pagination


class StaffRegisterRequest(BaseModel):
    id: int
    staff_id: int
    full_name: str
    car_sharing_phone_number: str
    console_phone_number: str
    created_at: datetime

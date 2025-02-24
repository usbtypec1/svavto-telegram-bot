import datetime
from dataclasses import dataclass
from typing import assert_never

from exceptions import ShiftAlreadyExistsError, StaffNotFoundError
from models import ExtraShiftItem, StaffIdAndDate
from repositories import ShiftRepository


@dataclass(frozen=True, slots=True, kw_only=True)
class ExtraShiftCreateInteractor:
    shift_repository: ShiftRepository
    staff_id: int
    date: datetime.date

    async def execute(self) -> ExtraShiftItem:
        shifts_to_create = [
            StaffIdAndDate(staff_id=self.staff_id, date=self.date),
        ]
        shifts_create_result = await self.shift_repository.create_extra(
            shifts=shifts_to_create,
        )
        if shifts_create_result.conflict_shifts:
            conflict_dates = [
                shift.date.isoformat()
                for shift in shifts_create_result.conflict_shifts
            ]
            raise ShiftAlreadyExistsError(
                message="Staff already has shift on this date",
                conflict_dates=conflict_dates,
            )
        if shifts_create_result.missing_staff_ids:
            raise StaffNotFoundError
        if shifts_create_result.created_shifts:
            return shifts_create_result.created_shifts[0]
        raise assert_never(shifts_create_result)

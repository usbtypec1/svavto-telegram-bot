import datetime
from collections.abc import Iterable
from dataclasses import dataclass

from enums import ShiftType
from models import ShiftListItem
from repositories import ShiftRepository

__all__ = ('ShiftsOfStaffForPeriodReadInteractor',)


@dataclass(frozen=True, slots=True, kw_only=True)
class ShiftsOfStaffForPeriodReadInteractor:
    shift_repository: ShiftRepository
    from_date: datetime.date
    to_date: datetime.date
    staff_ids: Iterable[int]
    shift_types: Iterable[ShiftType]

    async def execute(self):
        shifts: list[ShiftListItem] = []
        limit: int = 1000
        offset: int = 0
        while True:
            shifts_page = await self.shift_repository.get_list(
                from_date=self.from_date,
                to_date=self.to_date,
                limit=limit,
                offset=offset,
                staff_ids=self.staff_ids,
                shift_types=self.shift_types,
            )
            shifts += shifts_page.shifts
            if shifts_page.is_end_of_list_reached:
                break
            offset += limit

        return shifts

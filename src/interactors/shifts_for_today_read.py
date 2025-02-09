import datetime
from dataclasses import dataclass

from models import ShiftListItem
from repositories import ShiftRepository

__all__ = ('ShiftsForSpecificDateReadInteractor',)


@dataclass(frozen=True, slots=True, kw_only=True)
class ShiftsForSpecificDateReadInteractor:
    shift_repository: ShiftRepository
    date: datetime.date

    async def execute(self):
        shifts: list[ShiftListItem] = []
        while True:
            shifts_page = await self.shift_repository.get_list(
                from_date=self.date,
                to_date=self.date,
                limit=1000,
            )
            shifts += shifts_page.shifts
            if shifts_page.is_end_of_list_reached:
                break

        return shifts

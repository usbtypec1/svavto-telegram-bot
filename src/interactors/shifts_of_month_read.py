from dataclasses import dataclass

import pendulum

from enums import ShiftType
from models import ShiftListItem
from repositories import ShiftRepository


__all__ = ('ShiftsOfMonthReadInteractor',)


@dataclass(frozen=True, slots=True, kw_only=True)
class ShiftsOfMonthReadInteractor:
    shift_repository: ShiftRepository
    month: int
    year: int
    staff_id: int

    async def execute(self):
        from_date = pendulum.date(self.year, self.month, 1)
        to_date = from_date.end_of('month')

        shifts: list[ShiftListItem] = []
        limit: int = 1000
        offset: int = 0
        while True:
            shifts_page = await self.shift_repository.get_list(
                from_date=from_date,
                to_date=to_date,
                limit=limit,
                offset=offset,
                staff_ids=(self.staff_id,),
                shift_types=(
                    ShiftType.EXTRA,
                    ShiftType.REGULAR,
                    ShiftType.TEST,
                ),
            )
            shifts += shifts_page.shifts
            if shifts_page.is_end_of_list_reached:
                break
            offset += limit

        return shifts

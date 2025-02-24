from dataclasses import dataclass
from zoneinfo import ZoneInfo

from enums import ShiftType
from exceptions import ShiftNotFoundError
from models import ShiftListItem
from repositories import ShiftRepository
from services.shifts import get_current_shift_date


@dataclass(frozen=True, slots=True, kw_only=True)
class ShiftForTodayReadInteractor:
    shift_repository: ShiftRepository
    staff_id: int
    timezone: ZoneInfo

    async def execute(self) -> ShiftListItem:
        shift_date = get_current_shift_date(self.timezone)
        shifts_page = await self.shift_repository.get_list(
            from_date=shift_date,
            to_date=shift_date,
            staff_ids=(self.staff_id,),
            shift_types=(ShiftType.REGULAR, ShiftType.EXTRA),
        )
        if not shifts_page.shifts:
            raise ShiftNotFoundError
        return shifts_page.shifts[0]

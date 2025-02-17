from collections.abc import Iterable
from zoneinfo import ZoneInfo

from callback_data import StaffWithoutShiftsMonthChooseCallbackData
from models import AvailableDate, StaffWithoutShifts
from ui.views.available_months import AvailableMonthsListView, MONTH_NAMES
from ui.views.base import TextView

__all__ = ('StaffWithoutShiftsMonthChooseView', 'StaffWithoutShiftsView')


class StaffWithoutShiftsMonthChooseView(AvailableMonthsListView):

    def __init__(
            self,
            *,
            available_months: Iterable[AvailableDate],
            timezone: ZoneInfo,
    ) -> None:
        super().__init__(
            available_months=available_months,
            timezone=timezone,
            callback_data_factory=StaffWithoutShiftsMonthChooseCallbackData,
        )


class StaffWithoutShiftsView(TextView):

    def __init__(self, staff_without_shifts: StaffWithoutShifts):
        self.__staff_without_shifts = staff_without_shifts

    def get_text(self) -> str:
        month = MONTH_NAMES[self.__staff_without_shifts.month - 1]

        if not self.__staff_without_shifts.staff_list:
            return f'Нет сотрудников без смен на {month}'

        lines: list[str] = [f'<b>Сотрудники без смен на {month}</b>']
        for staff in self.__staff_without_shifts.staff_list:
            lines.append(f'• {staff.full_name}')

        return '\n'.join(lines)

from aiogram.filters.callback_data import CallbackData

from callback_data.prefixes import CallbackDataPrefix

__all__ = ('StaffWithoutShiftsMonthChooseCallbackData',)


class StaffWithoutShiftsMonthChooseCallbackData(
    CallbackData,
    prefix=CallbackDataPrefix.SUPERVISION_STAFF_WITHOUT_SHIFTS_MONTH,
):
    month: int
    year: int

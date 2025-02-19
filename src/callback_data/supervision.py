from aiogram.filters.callback_data import CallbackData

from callback_data.prefixes import CallbackDataPrefix

__all__ = ('DeadSoulsMonthChooseCallbackData',)


class DeadSoulsMonthChooseCallbackData(
    CallbackData,
    prefix=CallbackDataPrefix.SUPERVISION_DEAD_SOULS,
):
    month: int
    year: int

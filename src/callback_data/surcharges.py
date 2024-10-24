from aiogram.filters.callback_data import CallbackData

from callback_data.prefixes import CallbackDataPrefix

__all__ = ('PenaltyCreateChooseStaffCallbackData',)


class PenaltyCreateChooseStaffCallbackData(
    CallbackData,
    prefix=CallbackDataPrefix.PENALTY_CREATE_CHOOSE_STAFF,
):
    staff_id: int

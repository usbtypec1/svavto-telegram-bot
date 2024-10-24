from aiogram.filters.callback_data import CallbackData

from callback_data.prefixes import CallbackDataPrefix
from enums import PenaltyReason

__all__ = (
    'PenaltyCreateChooseStaffCallbackData',
    'PenaltyCreateChooseReasonCallbackData',
)


class PenaltyCreateChooseStaffCallbackData(
    CallbackData,
    prefix=CallbackDataPrefix.PENALTY_CREATE_CHOOSE_STAFF,
):
    staff_id: int


class PenaltyCreateChooseReasonCallbackData(
    CallbackData,
    prefix=CallbackDataPrefix.PENALTY_CREATE_CHOOSE_REASON,
):
    reason: PenaltyReason

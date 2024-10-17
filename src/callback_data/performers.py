from aiogram.filters.callback_data import CallbackData

from callback_data.prefixes import CallbackDataPrefix
from enums import StaffUpdateAction

__all__ = (
    'PerformerRegisterCallbackData',
    'StaffDetailCallbackData',
    'StaffUpdateCallbackData',
)


class PerformerRegisterCallbackData(
    CallbackData,
    prefix=CallbackDataPrefix.PERFORMER_REGISTER,
):
    telegram_id: int


class StaffDetailCallbackData(
    CallbackData,
    prefix=CallbackDataPrefix.STAFF_DETAIL,
):
    telegram_id: int


class StaffUpdateCallbackData(
    CallbackData,
    prefix=CallbackDataPrefix.STAFF_UPDATE,
):
    telegram_id: int
    action: StaffUpdateAction

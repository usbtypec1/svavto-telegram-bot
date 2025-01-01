from aiogram.filters.callback_data import CallbackData

from callback_data.prefixes import CallbackDataPrefix
from enums import StaffUpdateAction

__all__ = (
    'StaffDetailCallbackData',
    'StaffUpdateCallbackData',
    'StaffListCallbackData',
)


class StaffDetailCallbackData(
    CallbackData,
    prefix=CallbackDataPrefix.STAFF_DETAIL,
):
    staff_id: int
    include_banned: bool
    limit: int
    offset: int


class StaffUpdateCallbackData(
    CallbackData,
    prefix=CallbackDataPrefix.STAFF_UPDATE,
):
    staff_id: int
    action: StaffUpdateAction
    include_banned: bool
    limit: int
    offset: int


class StaffListCallbackData(CallbackData, prefix=CallbackDataPrefix.STAFF_LIST):
    include_banned: bool
    limit: int
    offset: int

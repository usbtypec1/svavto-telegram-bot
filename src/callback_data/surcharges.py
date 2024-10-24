from aiogram.filters.callback_data import CallbackData

from callback_data.prefixes import CallbackDataPrefix

__all__ = ('SurchargeCreateChooseStaffCallbackData',)


class SurchargeCreateChooseStaffCallbackData(
    CallbackData,
    prefix=CallbackDataPrefix.SURCHARGE_CREATE_CHOOSE_STAFF,
):
    staff_id: int

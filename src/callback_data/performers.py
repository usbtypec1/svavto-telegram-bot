from aiogram.filters.callback_data import CallbackData

from callback_data.prefixes import CallbackDataPrefix

__all__ = ('PerformerRegisterCallbackData',)


class PerformerRegisterCallbackData(
    CallbackData,
    prefix=CallbackDataPrefix.PERFORMER_REGISTER,
):
    telegram_id: int

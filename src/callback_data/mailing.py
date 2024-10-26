from aiogram.filters.callback_data import CallbackData

from callback_data.prefixes import CallbackDataPrefix
from enums import MailingType

__all__ = ('MailingTypeChooseCallbackData',)


class MailingTypeChooseCallbackData(
    CallbackData,
    prefix=CallbackDataPrefix.MAILING,
):
    type: MailingType

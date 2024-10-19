from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from callback_data.prefixes import CallbackDataPrefix
from views.base import TextView

__all__ = ('StaffScheduleMenu',)


class StaffScheduleMenu(TextView):
    text = 'График работы'
    reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='📆 Мой график',
                    callback_data=CallbackDataPrefix.SHIFT_OWN,
                ),
                InlineKeyboardButton(
                    text='✏️ Записаться на смены',
                    callback_data=CallbackDataPrefix.SHIFT_CREATE,
                ),
            ]
        ]
    )

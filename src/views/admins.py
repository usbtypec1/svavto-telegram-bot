from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from views.base import TextView
from views.button_texts import ButtonText

__all__ = ('AdminMenuView',)


class AdminMenuView(TextView):
    text = 'Меню старшего смены'
    reply_markup = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [
                KeyboardButton(text=ButtonText.STAFF_LIST),
                KeyboardButton(text=ButtonText.REPORTS),
            ],
            [
                KeyboardButton(text=ButtonText.SHIFTS_TODAY),
                KeyboardButton(text=ButtonText.SHIFTS),
                KeyboardButton(text=ButtonText.CAR_WASH_LIST),
            ],
            [
                KeyboardButton(text=ButtonText.PENALTY),
                KeyboardButton(text=ButtonText.SURCHARGE),
            ],
            [
                KeyboardButton(text=ButtonText.STAFF_PERFORMANCE),
                KeyboardButton(text=ButtonText.UNDERFILLING),
                KeyboardButton(text=ButtonText.MAILING),
            ],
        ]
    )

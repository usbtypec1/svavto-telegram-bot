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
                KeyboardButton(text=ButtonText.SHIFT_CARS_COUNT_BY_STAFF),
                KeyboardButton(
                    text=ButtonText.SHIFT_CARS_WITHOUT_WINDSHIELD_WASHER,
                ),
                KeyboardButton(text=ButtonText.MAILING),
            ],
        ]
    )

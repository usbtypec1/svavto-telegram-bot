from aiogram.types import (
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    KeyboardButton,
)

from views.base import TextView
from views.button_texts import ButtonText

__all__ = ('MainMenuView', 'RegisterView')


class MainMenuView(TextView):
    text = 'Главное меню'
    reply_markup = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [
                KeyboardButton(text=ButtonText.SHIFT_START),
            ],
            [
                KeyboardButton(text=ButtonText.SHIFT_START_EXTRA),
                KeyboardButton(text=ButtonText.SHIFT_SCHEDULE),
            ],
            [
                KeyboardButton(text=ButtonText.REPORT_FOR_PERIOD),
            ],
        ],
    )


class RegisterView(TextView):
    text = 'Зарегистрируйтесь, чтобы начать работу'
    reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Зарегистрироваться',
                    callback_data='register',
                )
            ]
        ]
    )

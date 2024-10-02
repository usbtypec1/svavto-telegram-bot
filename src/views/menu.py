from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, \
    InlineKeyboardButton

from views.base import TextView

__all__ = ('MainMenuView', 'RegisterView')


class MainMenuView(TextView):
    text = 'Главное меню'
    reply_markup = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
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

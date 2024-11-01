from aiogram.types import (
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    KeyboardButton, WebAppInfo, )

from views.base import TextView
from views.button_texts import ButtonText

__all__ = ('MainMenuView', 'RegisterView', 'ShiftMenuView')


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


class ShiftMenuView(TextView):
    text = 'Меню смены'

    def __init__(self, web_app_base_url: str):
        self.__web_app_base_url = web_app_base_url

    def get_reply_markup(self) -> ReplyKeyboardMarkup:
        shift_add_car_button = KeyboardButton(
            text=ButtonText.SHIFT_ADD_CAR,
            web_app=WebAppInfo(
                url=f'{self.__web_app_base_url}/shifts/add-car',
            )
        )
        return ReplyKeyboardMarkup(
            is_persistent=True,
            keyboard=[
                [
                    shift_add_car_button,
                ],
                [
                    KeyboardButton(text=ButtonText.SHIFT_ADDITIONAL_SERVICES),
                    KeyboardButton(text=ButtonText.SHIFT_ADDED_CARS),
                ],
                [
                    KeyboardButton(text=ButtonText.SHIFT_CHANGE_CAR_WASH),
                ],
                [
                    KeyboardButton(text=ButtonText.SHIFT_END),
                ],
            ],
        )

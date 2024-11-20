from aiogram.types import (
    InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton,
    ReplyKeyboardMarkup, ReplyKeyboardRemove, WebAppInfo,
)

from views.base import TextView
from views.button_texts import ButtonText

__all__ = ('MainMenuView', 'RegisterView', 'ShiftMenuView', 'StaffBannedView')


class MainMenuView(TextView):
    text = 'Главное меню'

    def __init__(self, web_app_base_url: str):
        self.__web_app_base_url = web_app_base_url

    def get_reply_markup(self) -> ReplyKeyboardMarkup:
        report_web_app_url = f'{self.__web_app_base_url}/reports'
        return ReplyKeyboardMarkup(
            is_persistent=True,
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
                    KeyboardButton(
                        text=ButtonText.REPORT_FOR_PERIOD,
                        web_app=WebAppInfo(url=report_web_app_url),
                    ),
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
                url=f'{self.__web_app_base_url}/shifts/cars',
            )
        )
        return ReplyKeyboardMarkup(
            is_persistent=True,
            resize_keyboard=True,
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


class StaffBannedView(TextView):
    text = '❌ Вы заблокированы в боте'
    reply_markup = ReplyKeyboardRemove()

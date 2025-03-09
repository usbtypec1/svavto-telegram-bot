from aiogram.types import (
    InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton,
    ReplyKeyboardMarkup, ReplyKeyboardRemove, WebAppInfo,
)

from ui.views.base import TextView
from ui.views.button_texts import ButtonText


__all__ = ('MainMenuView', 'RegisterView', 'ShiftMenuView', 'StaffBannedView')


class MainMenuView(TextView):
    text = 'Главное меню'

    def __init__(self, *, staff_id: int, web_app_base_url: str):
        self.__staff_id = staff_id
        self.__web_app_base_url = web_app_base_url

    def get_reply_markup(self) -> ReplyKeyboardMarkup:
        report_web_app_url = (f'{self.__web_app_base_url}/reports/'
                              f'{self.__staff_id}')
        penalty_web_app_url = (
            f'{self.__web_app_base_url}/penalties/{self.__staff_id}'
        )
        surcharge_web_app_url = (
            f'{self.__web_app_base_url}/surcharges/{self.__staff_id}'
        )
        return ReplyKeyboardMarkup(
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
                        text=ButtonText.PENALTY_LIST,
                        web_app=WebAppInfo(url=penalty_web_app_url),
                    ),
                    KeyboardButton(
                        text=ButtonText.SURCHARGE_LIST,
                        web_app=WebAppInfo(url=surcharge_web_app_url),
                    ),
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

    def __init__(self, staff_id: int, web_app_base_url: str):
        self.__staff_id = staff_id
        self.__web_app_base_url = web_app_base_url

    def get_reply_markup(self) -> ReplyKeyboardMarkup:
        url = f'{self.__web_app_base_url}/shifts/cars/create/{self.__staff_id}'
        shift_add_car_button = KeyboardButton(
            text=ButtonText.SHIFT_ADD_CAR,
            web_app=WebAppInfo(url=url)
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
                    KeyboardButton(
                        text=ButtonText.SHIFT_DRY_CLEANING_REQUEST,
                    )
                ],
                [
                    KeyboardButton(text=ButtonText.SHIFT_END),
                ],
            ],
        )


class StaffBannedView(TextView):
    text = '❌ Вы заблокированы в боте'
    reply_markup = ReplyKeyboardRemove()

from aiogram.types import (
    InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton,
    ReplyKeyboardMarkup, WebAppInfo,
)

from views.base import TextView
from views.button_texts import ButtonText

__all__ = ('AdminMenuView', 'AdminShiftsMenuView')


class AdminMenuView(TextView):
    text = 'Меню старшего смены'

    def __init__(self, web_app_base_url: str):
        self.__web_app_base_url = web_app_base_url

    def get_reply_markup(self) -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(
            resize_keyboard=True,
            keyboard=[
                [
                    KeyboardButton(text=ButtonText.STAFF_LIST),
                    KeyboardButton(text=ButtonText.REPORTS),
                ],
                [
                    KeyboardButton(
                        text=ButtonText.SHIFTS_TODAY,
                        web_app=WebAppInfo(
                            url=f'{self.__web_app_base_url}/shifts/confirm',
                        ),
                    ),
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


class AdminShiftsMenuView(TextView):
    text = '📆 Меню графиков'

    def __init__(self, web_app_base_url: str):
        self.__web_app_base_url = web_app_base_url

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        available_dates_button = InlineKeyboardButton(
            text=ButtonText.AVAILABLE_DATES,
            web_app=WebAppInfo(
                url=f'{self.__web_app_base_url}/shifts/available-dates',
            ),
        )
        shifts_table_button = InlineKeyboardButton(
            text=ButtonText.SHIFTS_TABLE,
            url='https://google.com',
        )
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [available_dates_button],
                [shifts_table_button],
            ]
        )
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    WebAppInfo,
)

from callback_data.prefixes import CallbackDataPrefix
from views.base import TextView
from views.button_texts import ButtonText

__all__ = ('AdminMenuView', 'AdminShiftsMenuView', 'AdminOtherMenuView')


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
                ],
                [
                    KeyboardButton(text=ButtonText.MAILING),
                    KeyboardButton(text=ButtonText.OTHER),
                ],
            ]
        )


class AdminShiftsMenuView(TextView):
    text = '📆 Меню графиков'

    def __init__(self, web_app_base_url: str):
        self.__web_app_base_url = web_app_base_url

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        available_dates_button = InlineKeyboardButton(
            text='📅 Открыть запись на смены',
            web_app=WebAppInfo(
                url=f'{self.__web_app_base_url}/shifts/available-dates',
            ),
        )
        shifts_table_url = (
            'https://docs.google.com/spreadsheets/d/'
            '1ktxCfMcepMwsZvP9r5BcvMSPNA2NTcYb'
        )
        shifts_table_button = InlineKeyboardButton(
            text='📊 Таблица',
            url=shifts_table_url,
        )
        shifts_edit_button = InlineKeyboardButton(
            text='✏️ Редактировать смены',
            web_app=WebAppInfo(
                url=f'{self.__web_app_base_url}/shifts/schedules',
            ),
        )
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [available_dates_button],
                [shifts_edit_button],
                [shifts_table_button],
            ]
        )


class AdminOtherMenuView(TextView):
    text = '🔧 Другое'

    def __init__(self, web_app_base_url: str):
        self.__web_app_base_url = web_app_base_url

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        direct_shift = InlineKeyboardButton(
            text='🚀 Выдать тестовый доступ',
            web_app=WebAppInfo(
                url=f'{self.__web_app_base_url}/shifts/direct-shift',
            ),
        )
        reports_button = InlineKeyboardButton(
            text='📊 Отчеты',
            callback_data=CallbackDataPrefix.REPORTS,
        )
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [direct_shift],
                [reports_button],
            ]
        )

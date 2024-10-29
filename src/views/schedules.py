from collections.abc import Iterable

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, \
    ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

from callback_data import StaffScheduleDetailCallbackData
from callback_data.prefixes import CallbackDataPrefix
from models import Staff
from views.base import TextView
from views.button_texts import ButtonText

__all__ = (
    'StaffScheduleMenu',
    'StaffListForScheduleView',
    'StaffScheduleDetailView',
)


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


class StaffListForScheduleView(TextView):
    text = 'Список сотрудников'

    def __init__(self, staff_list: Iterable[Staff]):
        self.__staff_list = tuple(staff_list)

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardBuilder()
        keyboard.max_width = 1

        for staff in self.__staff_list:
            keyboard.button(
                text=staff.full_name,
                callback_data=StaffScheduleDetailCallbackData(staff_id=staff.id)
            )

        return keyboard.as_markup()


class StaffScheduleDetailView(TextView):

    def __init__(self, staff: Staff, web_app_base_url: str):
        self.__staff = staff
        self.__web_app_base_url = web_app_base_url

    def get_text(self) -> str:
        return (
            f'Сотрудник: {self.__staff.full_name}'
        )

    def get_reply_markup(self) -> ReplyKeyboardMarkup:
        available_dates_url = (
            f'{self.__web_app_base_url}/shifts/schedules/{self.__staff.id}'
        )
        available_dates_button = KeyboardButton(
            text=ButtonText.AVAILABLE_DATES,
            web_app=WebAppInfo(url=available_dates_url),
        )
        main_menu_button = KeyboardButton(text=ButtonText.MAIN_MENU)

        return ReplyKeyboardMarkup(
            resize_keyboard=True,
            keyboard=[
                [available_dates_button],
                [main_menu_button],
            ]
        )

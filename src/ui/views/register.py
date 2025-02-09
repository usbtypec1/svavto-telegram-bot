from aiogram.types import (
    InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton,
    ReplyKeyboardMarkup, WebAppInfo,
)

from ui.views.base import TextView
from ui.views.button_texts import ButtonText

__all__ = (
    'StaffRegisterRequestNotificationView',
    'StaffRegisterView',
)


class StaffRegisterView(TextView):
    text = 'Зарегистрируйтесь, чтобы начать работу'

    def __init__(self, web_app_base_url: str):
        self.__web_app_base_url = web_app_base_url

    def get_reply_markup(self) -> ReplyKeyboardMarkup:
        url = f'{self.__web_app_base_url}/register-requests/create'
        button = KeyboardButton(
            text=ButtonText.REGISTER,
            web_app=WebAppInfo(
                url=url,
            )
        )
        return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[[button]])


class StaffRegisterRequestNotificationView(TextView):
    text = '❗️ Новый запрос на регистрацию'

    def __init__(self, web_app_base_url: str):
        self.__web_app_base_url = web_app_base_url

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        web_app_url = f'{self.__web_app_base_url}/register-requests'
        button = InlineKeyboardButton(
            text='📝 Список запросов на регистрацию',
            web_app=WebAppInfo(url=web_app_url)
        )
        return InlineKeyboardMarkup(inline_keyboard=[[button]])

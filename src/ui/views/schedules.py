from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from ui.views.base import TextView
from ui.views.button_texts import ButtonText

__all__ = ('StaffScheduleMenu',)


class StaffScheduleMenu(TextView):
    text = 'График работы'

    def __init__(self, web_app_base_url: str):
        self.__web_app_base_url = web_app_base_url

    def get_reply_markup(self) -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(
            resize_keyboard=True,
            keyboard=[
                [
                    KeyboardButton(text=ButtonText.SHIFT_MONTH_LIST),
                    KeyboardButton(text=ButtonText.SHIFT_APPLY),
                ],
                [
                    KeyboardButton(text=ButtonText.MAIN_MENU),
                ],
            ]
        )

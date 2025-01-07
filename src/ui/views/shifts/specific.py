from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, WebAppInfo

from ui.views.base import TextView

__all__ = ('SpecificShiftPickerView',)

from ui.views.button_texts import ButtonText


class SpecificShiftPickerView(TextView):
    text = '📆 Выберите смену сотрудника'

    """
    Show reply keyboard with web app
    that allows to pick specific shift of specific staff member.
    """

    def __init__(self, *, web_app_base_url: str, staff_id: int):
        self.__web_app_base_url = web_app_base_url
        self.__staff_id = staff_id

    def get_reply_markup(self) -> ReplyKeyboardMarkup:
        web_app_url = (
            f'{self.__web_app_base_url}/shifts/{self.__staff_id}'
        )
        web_app_button = KeyboardButton(
            text=ButtonText.SPECIFIC_SHIFT,
            web_app=WebAppInfo(url=web_app_url),
        )
        return ReplyKeyboardMarkup(
            resize_keyboard=True,
            keyboard=[[web_app_button]],
        )

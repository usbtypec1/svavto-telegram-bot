from collections.abc import Iterable

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, WebAppInfo

from models import StaffIdAndName
from ui.views.base import TextView
from ui.views.button_texts import ButtonText

__all__ = (
    'SpecificShiftPickerView',
    'ShiftStartForSpecificDateRequestSentView',
)


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


class ShiftStartForSpecificDateRequestSentView(TextView):

    def __init__(self, staff_list: Iterable[StaffIdAndName]):
        self.__staff_list = tuple(staff_list)

    def get_text(self) -> str:
        if not self.__staff_list:
            return '❗️ Нет сотрудников для отправки запроса на начало смены'
        lines = [
            f'✅ Запросы на начало смены отправлены сотрудникам:',
        ]
        for i, staff in enumerate(self.__staff_list, start=1):
            lines.append(f'{i}. {staff.full_name}')
        return '\n'.join(lines)

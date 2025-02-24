from collections.abc import Iterable

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, WebAppInfo

from models import ShiftExtraCreateResult, ShiftListItem, StaffIdAndName
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

    def __init__(
            self,
            *,
            staff_list: Iterable[StaffIdAndName],
            existing_shifts: Iterable[ShiftListItem],
            created_extra_shifts_result: ShiftExtraCreateResult,
    ):
        self.__staff_list = tuple(staff_list)
        self.__existing_shifts = existing_shifts
        self.__created_extra_shifts_result = created_extra_shifts_result

    def get_text(self) -> str:
        staff_id_to_name = {
            staff.id: staff.full_name
            for staff in self.__staff_list
        }
        if not self.__staff_list:
            return '❗️ Нет сотрудников для отправки запроса на начало смены'
        lines = [
            f'✅ Запросы на начало смены отправлены сотрудникам:',
        ]
        for i, shift in enumerate(self.__existing_shifts, start=1):
            lines.append(f'{i}. {shift.staff_full_name}')

        if self.__created_extra_shifts_result.created_shifts:
            lines.append('\n✅ Доп.смены созданы для:')
            for i, shift in enumerate(
                    self.__created_extra_shifts_result.created_shifts,
                    start=1,
            ):
                lines.append(f'{i}. {staff_id_to_name[shift.staff_id]}')

        if self.__created_extra_shifts_result.missing_staff_ids:
            lines.append('\n❗️ Незарегистрированные в системе сотрудники:')
            for i, staff_id in enumerate(
                    self.__created_extra_shifts_result.missing_staff_ids,
                    start=1,
            ):
                lines.append(f'{i}. {staff_id_to_name[staff_id]}')

        if self.__created_extra_shifts_result.conflict_shifts:
            lines.append('\n❗️ Неудачная попытка создать доп.смену для:')
            for i, shift in enumerate(
                    self.__created_extra_shifts_result.conflict_shifts,
                    start=1,
            ):
                lines.append(f'{i}. {staff_id_to_name[shift.staff_id]}')

        return '\n'.join(lines)

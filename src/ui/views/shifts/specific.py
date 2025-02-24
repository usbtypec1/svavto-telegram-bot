from collections.abc import Iterable, Mapping

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, WebAppInfo

from models import (
    ExtraShiftItem, ShiftExtraCreateResult, ShiftListItem,
    StaffIdAndDate, StaffIdAndName,
)
from ui.views.base import TextView
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


def format_existing_shifts(shifts: Iterable[ShiftListItem]) -> str:
    shifts = tuple(shifts)
    if not shifts:
        return '❗️ Нет смен для отправки запроса на подтверждение'
    lines: list[str] = ['✅ Запросы на начало смены отправлены сотрудникам:']
    for i, shift in enumerate(shifts, start=1):
        lines.append(f'{i}. {shift.staff_full_name}')
    return '\n'.join(lines)


def format_created_extra_shifts(
        shifts: Iterable[ExtraShiftItem],
        staff_id_to_name: Mapping[int, str],
) -> str:
    lines: list[str] = ['✅ Доп.смены созданы для:']
    for i, shift in enumerate(shifts, start=1):
        lines.append(f'{i}. {staff_id_to_name[shift.staff_id]}')
    return '\n'.join(lines)


def format_missing_staff(
        missing_staff_ids: Iterable[int],
        staff_id_to_name: Mapping[int, str],
) -> str:
    lines: list[str] = ['❌ Незарегистрированные в системе сотрудники:']
    for i, staff_id in enumerate(missing_staff_ids, start=1):
        lines.append(f'{i}. {staff_id_to_name[staff_id]}')
    return '\n'.join(lines)


def format_conflict_shifts(
        conflict_shifts: Iterable[StaffIdAndDate],
        staff_id_to_name: Mapping[int, str],
):
    lines: list[str] = ['❌ Неудачная попытка создать доп.смену для:']
    for i, shift in enumerate(conflict_shifts, start=1):
        lines.append(f'{i}. {staff_id_to_name[shift.staff_id]}')
    return '\n'.join(lines)


def format_created_shifts_result(
        shifts_create_result: ShiftExtraCreateResult,
        staff_id_to_name: Mapping[int, str],
) -> str:
    lines: list[str] = []
    if shifts_create_result.created_shifts:
        lines.append(
            format_created_extra_shifts(
                shifts=shifts_create_result.created_shifts,
                staff_id_to_name=staff_id_to_name,
            ),
        )
        lines.append('\n')

    if shifts_create_result.missing_staff_ids:
        lines.append(
            format_missing_staff(
                missing_staff_ids=shifts_create_result.missing_staff_ids,
                staff_id_to_name=staff_id_to_name,
            ),
        )
        lines.append('\n')

    if shifts_create_result.conflict_shifts:
        lines.append(
            format_conflict_shifts(
                conflict_shifts=shifts_create_result.conflict_shifts,
                staff_id_to_name=staff_id_to_name,
            ),
        )

    return '\n'.join(lines)


class ShiftStartForSpecificDateRequestSentView(TextView):

    def __init__(
            self,
            *,
            staff_list: Iterable[StaffIdAndName],
            existing_shifts: Iterable[ShiftListItem],
            created_extra_shifts_result: ShiftExtraCreateResult | None,
    ):
        self.__staff_list = tuple(staff_list)
        self.__existing_shifts = existing_shifts
        self.__created_extra_shifts_result = created_extra_shifts_result

    def get_text(self) -> str:
        if not self.__staff_list:
            return '❗️ Нет сотрудников для отправки запроса на начало смены'
        lines = [format_existing_shifts(self.__existing_shifts), '']
        if self.__created_extra_shifts_result is not None:
            staff_id_to_name = {
                staff.id: staff.full_name
                for staff in self.__staff_list
            }
            lines.append(
                format_created_shifts_result(
                    shifts_create_result=self.__created_extra_shifts_result,
                    staff_id_to_name=staff_id_to_name,
                ),
            )
        return '\n'.join(lines)

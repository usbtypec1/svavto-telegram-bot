import datetime
from collections.abc import Iterable
from typing import Final
from zoneinfo import ZoneInfo

from aiogram.types import (
    InlineKeyboardButton, InlineKeyboardMarkup,
    KeyboardButton, ReplyKeyboardMarkup, WebAppInfo,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

import ui.markups
from callback_data import (
    ExtraShiftCreateAcceptCallbackData,
    ExtraShiftCreateRejectCallbackData,
    ShiftApplyCallbackData,
    ShiftWorkTypeChoiceCallbackData,
)
from enums import ShiftType, ShiftWorkType
from models import (
    AvailableDate, ShiftListItem,
)
from ui.views.base import TextView
from ui.views.button_texts import ButtonText


__all__ = (
    'ShiftWorkTypeChoiceView',
    'shift_work_types_and_names',
    'ShiftApplyChooseMonthView',
    'ShiftApplyScheduleMonthCalendarWebAppView',
    'StaffShiftScheduleCreatedNotificationView',
    'StaffHasNoAnyCreatedShiftView',
    'ShiftsForMonthListView',
    'ExtraShiftScheduleWebAppView',
    'ExtraShiftScheduleNotificationView',
)

shift_work_types_and_names: tuple[tuple[ShiftWorkType, str], ...] = (
    (ShiftWorkType.MOVE_TO_WASH, 'Перегон ТС на мойку'),
    (ShiftWorkType.LIGHT_WASHES, 'Легкие мойки'),
    (ShiftWorkType.FIND_VEHICLE_IN_CITY, 'Поиск ТС в городе'),
    (ShiftWorkType.ASSIGNMENT_MOVE, 'Перегон по заданию'),
)


class ShiftWorkTypeChoiceView(TextView):
    text = 'Выберите направление, в котором хотите начать смену:'
    reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=shift_work_type_name,
                    callback_data=ShiftWorkTypeChoiceCallbackData(
                        work_type=shift_work_type,
                    ).pack(),
                )
            ]
            for shift_work_type, shift_work_type_name in
            shift_work_types_and_names
        ]
    )


month_names: Final[tuple[str, ...]] = (
    'январь',
    'февраль',
    'март',
    'апрель',
    'май',
    'июнь',
    'июль',
    'август',
    'сентябрь',
    'октябрь',
    'ноябрь',
    'декабрь',
)


class ShiftApplyChooseMonthView(TextView):

    def __init__(
            self,
            available_dates: Iterable[AvailableDate],
            timezone: ZoneInfo,
    ):
        self.__available_dates = tuple(available_dates)
        self.__timezone = timezone

    def get_text(self) -> str:
        if self.__available_dates:
            return '📆 Выберите месяц'
        return '❌ Нет доступных месяцев для записи на смену'

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardBuilder()
        keyboard.max_width = 1

        now = datetime.datetime.now(self.__timezone)

        for available_date in self.__available_dates:
            month_name = month_names[available_date.month - 1]

            if available_date.year == now.year:
                text = month_name
            else:
                text = f'{month_name} - {available_date.year} год'

            keyboard.button(
                text=text.capitalize(),
                callback_data=ShiftApplyCallbackData(
                    month=available_date.month,
                    year=available_date.year,
                ),
            )

        return keyboard.as_markup()


class ShiftApplyScheduleMonthCalendarWebAppView(TextView):

    def __init__(
            self,
            web_app_base_url: str,
            month: int,
            year: int,
    ):
        self.__web_app_base_url = web_app_base_url
        self.__month = month
        self.__year = year

    def get_text(self) -> str:
        month_name = month_names[self.__month - 1]
        return (
            f'📆 Выберите даты для выхода на смены за {month_name}'
            f' {self.__year} года'
        )

    def get_reply_markup(self) -> ReplyKeyboardMarkup:
        url = (
            f'{self.__web_app_base_url}/shifts/apply'
            f'?year={self.__year}&month={self.__month}'
        )
        return ReplyKeyboardMarkup(
            resize_keyboard=True,
            keyboard=[
                [
                    KeyboardButton(
                        text=ButtonText.SHIFT_SCHEDULE_MONTH_CALENDAR,
                        web_app=WebAppInfo(url=url)
                    ),
                ],
                [
                    KeyboardButton(text=ButtonText.MAIN_MENU),
                ],
            ],
        )


class StaffShiftScheduleCreatedNotificationView(TextView):

    def __init__(self, staff_full_name: str):
        self.__staff_full_name = staff_full_name

    def get_text(self) -> str:
        return f'Сотрудник {self.__staff_full_name} внес график работы'


class StaffHasNoAnyCreatedShiftView(TextView):
    text = '❗️ Вы еще не заполнили график'
    reply_markup = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [
                KeyboardButton(text=ButtonText.SHIFT_APPLY),
            ],
            [
                KeyboardButton(text=ButtonText.MAIN_MENU),
            ],
        ],
    )


class ShiftsForMonthListView(TextView):

    def __init__(
            self,
            *,
            month: int,
            year: int,
            shifts: Iterable[ShiftListItem],
    ):
        self.__month = month
        self.__year = year
        self.__shifts = tuple(shifts)

    def get_text(self) -> str:
        month = month_names[self.__month - 1]
        lines: list[str] = [f'<b>📆 График за {month}</b>']

        if not self.__shifts:
            lines.append('❌ Нет смен')

        shifts_sorted_by_date = sorted(
            self.__shifts,
            key=lambda shift: shift.date,
        )
        for i, shift in enumerate(shifts_sorted_by_date, start=1):
            if shift.type == ShiftType.EXTRA:
                shift_type = '(доп)'
            elif shift.type == ShiftType.TEST:
                shift_type = '(тест)'
            else:
                shift_type = ''
            lines.append(f'{i}. {shift.date:%d.%m.%Y} {shift_type}'.strip())

        return '\n'.join(lines)


class ExtraShiftScheduleWebAppView(TextView):
    text = '📆 Выберите дату'

    def __init__(self, web_app_base_url: str):
        self.__web_app_base_url = web_app_base_url

    def get_reply_markup(self) -> ReplyKeyboardMarkup:
        url = f'{self.__web_app_base_url}/shifts/extra'
        return ReplyKeyboardMarkup(
            resize_keyboard=True,
            keyboard=[
                [
                    KeyboardButton(
                        text=ButtonText.EXTRA_SHIFT_CALENDAR,
                        web_app=WebAppInfo(url=url),
                    ),
                ],
                [
                    KeyboardButton(text=ButtonText.MAIN_MENU),
                ],
            ],
        )


class ExtraShiftScheduleNotificationView(TextView):

    def __init__(
            self,
            staff_id: int,
            staff_full_name: str,
            shift_date: datetime.date,
    ):
        self.__staff_id = staff_id
        self.__staff_full_name = staff_full_name
        self.__shift_date = shift_date

    def get_text(self) -> str:
        return (
            f'Сотрудник {self.__staff_full_name} запросил доп.смену'
            f' на дату {self.__shift_date:%d.%m.%Y}'
        )

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        return ui.markups.create_confirm_reject_markup(
            confirm_callback_data=ExtraShiftCreateAcceptCallbackData(
                staff_id=self.__staff_id,
                date=self.__shift_date.isoformat(),
            ),
            reject_callback_data=ExtraShiftCreateRejectCallbackData(
                staff_id=self.__staff_id,
                date=self.__shift_date.isoformat(),
            ),
        )

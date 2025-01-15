import datetime
from typing import Protocol

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

import ui
from callback_data import (
    ExtraShiftStartCallbackData,
    ShiftImmediateStartCallbackData,
    ShiftRejectCallbackData,
    ShiftStartCallbackData,
    ShiftStartRequestAcceptCallbackData,
    ShiftStartRequestRejectCallbackData,
)
from models import ShiftListItem, Staff
from ui.views.base import TextView

__all__ = (
    'StaffReadyToStartShiftRequestView',
    'ShiftImmediateStartRequestView',
    'ExtraShiftStartView',
    'ShiftStartConfirmView',
)


class HasIdAndDate(Protocol):
    id: int
    date: datetime.date


class StaffReadyToStartShiftRequestView(TextView):

    def __init__(self, *, staff: Staff, shift: ShiftListItem):
        self.__staff = staff
        self.__shift = shift

    def get_text(self) -> str:
        return (
            f'📆 Сотрудник {self.__staff.full_name}'
            f' хочет начать сегодняшнюю смену'
        )

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        accept_callback_data = ShiftStartRequestAcceptCallbackData(
            shift_id=self.__shift.id,
        )
        reject_callback_data = ShiftStartRequestRejectCallbackData(
            shift_id=self.__shift.id,
        )
        return ui.markups.create_accept_reject_markup(
            accept_callback_data=accept_callback_data,
            reject_callback_data=reject_callback_data,
        )


class ShiftImmediateStartRequestView(TextView):

    def __init__(self, *, date: datetime.date):
        self.__date = date

    def get_text(self) -> str:
        return f'📆 Начните смену на дату {self.__date:%d.%m.%Y}'

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        button = InlineKeyboardButton(
            text='🚀 Начать смену',
            callback_data=ShiftImmediateStartCallbackData(
                date=self.__date.isoformat(),
            ).pack()
        )
        return InlineKeyboardMarkup(inline_keyboard=[[button]])


class ExtraShiftStartView(TextView):

    def __init__(
            self,
            staff_full_name: str,
            shift_date: datetime.date,
    ):
        self.__staff_full_name = staff_full_name
        self.__shift_date = shift_date

    def get_text(self) -> str:
        return (
            f'✅ {self.__staff_full_name}, ваш запрос на доп.смену на дату'
            f' {self.__shift_date:%d.%m.%Y} подтвержден'
        )

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        button = InlineKeyboardButton(
            text='🚀 Начать доп.смену',
            callback_data=ExtraShiftStartCallbackData(
                date=self.__shift_date.isoformat(),
            ).pack(),
        )
        return InlineKeyboardMarkup(inline_keyboard=[[button]])


class ShiftStartConfirmView(TextView):

    def __init__(self, shift_id: int, staff_full_name: str):
        self.__shift_id = shift_id
        self.__staff_full_name = staff_full_name

    def get_text(self) -> str:
        return f'{self.__staff_full_name} подтвердите выход на смену'

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        accept_callback_data = ShiftStartCallbackData(shift_id=self.__shift_id)
        reject_callback_data = ShiftRejectCallbackData(shift_id=self.__shift_id)
        return ui.markups.create_accept_reject_markup(
            accept_callback_data=accept_callback_data,
            reject_callback_data=reject_callback_data,
        )

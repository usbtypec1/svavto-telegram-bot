import datetime

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

import ui
from callback_data import (
    ExtraShiftStartCallbackData, ShiftRegularRejectCallbackData,
    ShiftRegularStartCallbackData, TestShiftStartCallbackData,
)
from ui.views.base import TextView

__all__ = (
    'TestShiftStartRequestView',
    'ShiftExtraStartRequestConfirmedView',
    'ShiftRegularStartRequestView',
)


class TestShiftStartRequestView(TextView):
    """
    Admin sends this view to staff to ask them to start a test shift.
    """

    def __init__(self, *, date: datetime.date):
        self.__date = date

    def get_text(self) -> str:
        return f'📆 Начните тестовую смену на дату {self.__date:%d.%m.%Y}'

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        button = InlineKeyboardButton(
            text='🚀 Начать тестовую смену',
            callback_data=TestShiftStartCallbackData(
                date=self.__date.isoformat(),
            ).pack()
        )
        return InlineKeyboardMarkup(inline_keyboard=[[button]])


class ShiftExtraStartRequestConfirmedView(TextView):
    """
    Staff receives this view
    after admin confirms their request to start an extra shift.
    """

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


class ShiftRegularStartRequestView(TextView):
    """
    Admin sends this view to staff to ask them to start a regular shift.
    """

    def __init__(
            self,
            *,
            shift_id: int,
            shift_date: datetime.date,
            staff_full_name: str,
    ):
        self.__shift_id = shift_id
        self.__shift_date = shift_date
        self.__staff_full_name = staff_full_name

    def get_text(self) -> str:
        return (
            f'{self.__staff_full_name} подтвердите выход на смену на дату'
            f' {self.__shift_date:%d.%m.%Y}'
        )

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        accept_callback_data = ShiftRegularStartCallbackData(
            shift_id=self.__shift_id)
        reject_callback_data = ShiftRegularRejectCallbackData(
            shift_id=self.__shift_id)
        return ui.markups.create_confirm_reject_markup(
            confirm_callback_data=accept_callback_data,
            reject_callback_data=reject_callback_data,
        )

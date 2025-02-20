import datetime

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from callback_data import TestShiftStartCallbackData
from ui.views.base import TextView


__all__ = ('TestShiftStartRequestView',)


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

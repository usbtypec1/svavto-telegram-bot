import datetime

from aiogram.types import InlineKeyboardMarkup

from callback_data import (
    ShiftRegularRejectCallbackData,
    ShiftRegularStartCallbackData,
)
from ui.markups import create_confirm_reject_markup
from ui.views.base import TextView


__all__ = ('ShiftRegularStartRequestView',)


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
            shift_id=self.__shift_id
        )
        reject_callback_data = ShiftRegularRejectCallbackData(
            shift_id=self.__shift_id
        )
        return create_confirm_reject_markup(
            confirm_callback_data=accept_callback_data,
            reject_callback_data=reject_callback_data,
        )

import datetime
from typing import Protocol

from aiogram.types import InlineKeyboardMarkup

from callback_data import (
    ShiftConfirmCallbackData,
    ShiftRejectCallbackData,
)
from enums import ShiftType
from ui.markups import create_confirm_reject_markup
from ui.views import TextView


class HasIdAndDateAndType(Protocol):
    id: int
    date: datetime.date
    type: ShiftType


class ShiftConfirmRequestView(TextView):

    def __init__(self, shift: HasIdAndDateAndType):
        self.__shift = shift

    def get_text(self) -> str:
        shift_date = self.__shift.date.strftime('%d.%m.%Y')
        if self.__shift.type == ShiftType.EXTRA:
            return f'❗️ Подтвердите выход на доп.смену на {shift_date}'
        return f'❗️ Подтвердите выход на смену на {shift_date}'

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        confirm_callback_data = ShiftConfirmCallbackData(
            shift_id=self.__shift.id,
        )
        reject_callback_data = ShiftRejectCallbackData(
            shift_id=self.__shift.id,
        )
        return create_confirm_reject_markup(
            confirm_callback_data=confirm_callback_data,
            reject_callback_data=reject_callback_data,
        )

import datetime
from collections.abc import Iterable

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from models import ShiftListItem
from ui.views import ButtonText, TextView

__all__ = ('SupervisionShiftConfirmationsView', 'SupervisionMenuView')


class SupervisionMenuView(TextView):
    text = '🔍 Меню контроля'
    reply_markup = ReplyKeyboardMarkup(
        is_persistent=True,
        resize_keyboard=True,
        keyboard=[
            [
                KeyboardButton(text=ButtonText.SUPERVISION_CAR_TRANSFERS),
                KeyboardButton(text=ButtonText.SUPERVISION_SHIFT_CONFIRMATIONS),
            ],
            [
                KeyboardButton(
                    text=ButtonText.SUPERVISION_STAFF_WITHOUT_SHIFTS,
                ),
            ],
            [
                KeyboardButton(text=ButtonText.MAIN_MENU)
            ],
        ],
    )


class SupervisionShiftConfirmationsView(TextView):

    def __init__(
            self,
            *,
            shift_date: datetime.date,
            shifts: Iterable[ShiftListItem],
    ):
        self.__shift_date = shift_date
        self.__shifts = tuple(shifts)

    def get_text(self) -> str:
        formatted_date = f'{self.__shift_date:%d.%m.%Y}'
        if not self.__shifts:
            return f'😔 Нет смен на {formatted_date}'

        lines: list[str] = [f'<b>📆 Подтверждения смен на {formatted_date}</b>']

        for shift in self.__shifts:

            is_rejected = shift.rejected_at is not None
            is_started = shift.started_at is not None

            if is_started:
                emoji = '✅'
            elif is_rejected:
                emoji = '❌'
            else:
                emoji = '➖'

            lines.append(f'{emoji} {shift.staff_full_name}')

        return '\n'.join(lines)

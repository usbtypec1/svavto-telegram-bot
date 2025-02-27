import datetime
from collections.abc import Iterable
from typing import Final, Protocol
from zoneinfo import ZoneInfo

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from ui.views.base import TextView


__all__ = ('MONTH_NAMES', 'AvailableMonthsListView')

MONTH_NAMES: Final[tuple[str, ...]] = (
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


class MonthAndYear(Protocol):
    month: int
    year: int


class AvailableMonthsListView(TextView):

    def __init__(
            self,
            *,
            available_months: Iterable[MonthAndYear],
            timezone: ZoneInfo,
            callback_data_factory: type[CallbackData],
    ) -> None:
        self.__available_months = tuple(available_months)
        self.__timezone = timezone
        self.__callback_data_factory = callback_data_factory

    def get_text(self) -> str:
        if self.__available_months:
            return '📆 Выберите месяц'
        return '❌ Нет доступных месяцев'

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardBuilder()
        keyboard.max_width = 1

        now = datetime.datetime.now(self.__timezone)

        for available_date in self.__available_months:
            month_name = MONTH_NAMES[available_date.month - 1]

            if available_date.year == now.year:
                text = month_name
            else:
                text = f'{month_name} - {available_date.year} год'

            keyboard.button(
                text=text.capitalize(),
                callback_data=self.__callback_data_factory(
                    month=available_date.month,
                    year=available_date.year,
                ),
            )

        return keyboard.as_markup()

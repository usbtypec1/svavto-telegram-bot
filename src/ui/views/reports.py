from typing import Iterable, Protocol

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from ui.views.base import TextView

__all__ = ('ReportTablesView',)


class HasNameAndUrl(Protocol):
    name: str
    url: str


class ReportTablesView(TextView):
    text = '📊 Отчеты'

    def __init__(
            self,
            report_tables: Iterable[HasNameAndUrl],
    ) -> None:
        self.__report_tables = report_tables

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardBuilder()
        keyboard.max_width = 1

        for report_table in self.__report_tables:
            keyboard.button(
                text=report_table.name,
                url=report_table.url,
            )

        return keyboard.as_markup()

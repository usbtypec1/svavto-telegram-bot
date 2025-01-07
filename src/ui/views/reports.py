from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from ui.views.base import TextView

__all__ = ('ReportsMenuView',)


class ReportsMenuView(TextView):
    text = '📊 Отчеты'

    def __init__(
            self,
            *,
            staff_revenue_report_table_url: str,
            service_costs_report_table_url: str,
    ):
        self.__staff_revenue_report_table_url = staff_revenue_report_table_url
        self.__service_costs_report_table_url = service_costs_report_table_url

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        staff_revenue_report_table_button = InlineKeyboardButton(
            text='📊 Таблица 1',
            url=self.__staff_revenue_report_table_url,
        )
        service_costs_report_table_button = InlineKeyboardButton(
            text='📊 Таблица 2',
            url=self.__service_costs_report_table_url,
        )
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [staff_revenue_report_table_button],
                [service_costs_report_table_button],
            ],
        )

from collections.abc import Iterable

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from callback_data import StaffDetailCallbackData, StaffUpdateCallbackData
from enums import StaffUpdateAction
from models import Staff
from views.base import TextView

__all__ = ('StaffListView', 'StaffDetailView')


class StaffListView(TextView):

    def __init__(self, staff_list: Iterable[Staff]):
        self.__staff_list = tuple(staff_list)

    def get_text(self) -> str:
        if not self.__staff_list:
            return '😔 Нет зарегистрированных сотрудников'
        return 'Список сотрудников'

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardBuilder()

        for staff in self.__staff_list:
            callback_data = StaffDetailCallbackData(
                telegram_id=staff.telegram_id,
            )
            button = InlineKeyboardButton(
                text=staff.full_name,
                callback_data=callback_data.pack()
            )
            keyboard.row(button)

        return keyboard.as_markup()


class StaffDetailView(TextView):

    def __init__(self, staff: Staff):
        self.__staff = staff

    def get_text(self) -> str:
        return (
            f'📱 <b>ID:</b> {self.__staff.telegram_id}\n'
            f'👤 <b>ФИО:</b> {self.__staff.full_name}\n'
            '📞 <b>Номер телефона в каршеринге:</b>'
            f' {self.__staff.car_sharing_phone_number}\n'
            '📞 <b>Номер телефона в Консоли:</b>'
            f' {self.__staff.console_phone_number}\n'
            f'📅 <b>Дата регистрации:</b>'
            f' {self.__staff.created_at:%d.%m.%Y %H:%M:%S}'
        )

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardBuilder()

        if self.__staff.is_banned:
            ban_button = InlineKeyboardButton(
                text='🔑 Разблокировать',
                callback_data=StaffUpdateCallbackData(
                    telegram_id=self.__staff.telegram_id,
                    action=StaffUpdateAction.UNBAN,
                ).pack(),
            )
            keyboard.row(ban_button)
        else:
            unban_button = InlineKeyboardButton(
                text='❌ Заблокировать',
                callback_data=StaffUpdateCallbackData(
                    telegram_id=self.__staff.telegram_id,
                    action=StaffUpdateAction.BAN,
                ).pack(),
            )
            keyboard.row(unban_button)

        return keyboard.as_markup()

from collections.abc import Iterable

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

from callback_data import StaffDetailCallbackData, StaffUpdateCallbackData
from callback_data.prefixes import CallbackDataPrefix
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
        return '👥 Список сотрудников'

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardBuilder()

        for staff in self.__staff_list:
            callback_data = StaffDetailCallbackData(
                telegram_id=staff.id,
            )
            button = InlineKeyboardButton(
                text=staff.full_name,
                callback_data=callback_data.pack()
            )
            keyboard.row(button)

        return keyboard.as_markup()


class StaffDetailView(TextView):

    def __init__(self, staff: Staff, web_app_base_url: str):
        self.__staff = staff
        self.__web_app_base_url = web_app_base_url

    def get_text(self) -> str:
        if self.__staff.is_banned:
            banned_status_line = '<b>❌ Заблокирован</b>\n'
        else:
            banned_status_line = ''

        return (
            f'📱 <b>ID:</b> {self.__staff.id}\n'
            f'👤 <b>ФИО:</b> {self.__staff.full_name}\n'
            '📞 <b>Номер телефона в каршеринге:</b>'
            f' {self.__staff.car_sharing_phone_number}\n'
            '📞 <b>Номер телефона в Консоли:</b>'
            f' {self.__staff.console_phone_number}\n'
            f'{banned_status_line}'
            f'📅 <b>Дата регистрации:</b>'
            f' {self.__staff.created_at:%d.%m.%Y %H:%M:%S}'
        )

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardBuilder()
        keyboard.max_width = 1

        if self.__staff.is_banned:
            keyboard.button(
                text='🔑 Разблокировать',
                callback_data=StaffUpdateCallbackData(
                    telegram_id=self.__staff.id,
                    action=StaffUpdateAction.UNBAN,
                ),
            )
        else:
            keyboard.button(
                text='❌ Заблокировать',
                callback_data=StaffUpdateCallbackData(
                    telegram_id=self.__staff.id,
                    action=StaffUpdateAction.BAN,
                ),
            )
        keyboard.button(
            text='🛑 Штрафы',
            web_app=WebAppInfo(
                url=f'{self.__web_app_base_url}/penalties/{self.__staff.id}',
            ),
        )
        keyboard.button(
            text='🔙 Назад',
            callback_data=CallbackDataPrefix.STAFF_LIST,
        )

        return keyboard.as_markup()

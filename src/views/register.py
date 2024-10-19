from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from callback_data.prefixes import CallbackDataPrefix
from models import StaffToCreate
from views.base import TextView

__all__ = ('StaffRegisterConfirmView', 'StaffRegisterNotificationView')


class StaffRegisterConfirmView(TextView):

    def __init__(
            self,
            full_name: str,
            car_sharing_phone_number: str,
            console_phone_number: str,
    ):
        self.__full_name = full_name
        self.__car_sharing_phone_number = car_sharing_phone_number
        self.__console_phone_number = console_phone_number

    def get_text(self) -> str:
        return (
            f'Подтвердите введенные данные:\n'
            f'ФИО: {self.__full_name}\n'
            f'Номер телефона в каршеринге: {self.__car_sharing_phone_number}\n'
            f'Номер телефона в Консоли: {self.__console_phone_number}\n'
        )

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text='Начать заново',
                        callback_data='register',
                    ),
                    InlineKeyboardButton(
                        text='Подтвердить',
                        callback_data='register-confirm'
                    ),
                ],
            ],
        )


class StaffRegisterNotificationView(TextView):

    def __init__(self, staff: StaffToCreate):
        self.__staff = staff

    def get_text(self) -> str:
        return (
            'Новый пользователь хочет зарегистрироваться\n'
            f'<b>🆔 ID:</b> {self.__staff.id}\n'
            f'<b>👤 ФИО:</b> {self.__staff.full_name}\n'
            '<b>📲 Номер телефона в каршеринге:</b>'
            f' {self.__staff.car_sharing_phone_number}\n'
            '<b>📲 Номер телефона в компании Консоль:</b>'
            f' {self.__staff.console_phone_number}'
        )

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        accept_button = InlineKeyboardButton(
            text='✅ Зарегистрировать',
            callback_data=CallbackDataPrefix.STAFF_REGISTER_ACCEPT,
        )
        reject_button = InlineKeyboardButton(
            text='❌ Отклонить',
            callback_data=CallbackDataPrefix.STAFF_REGISTER_REJECT,
        )
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [reject_button, accept_button],
            ],
        )

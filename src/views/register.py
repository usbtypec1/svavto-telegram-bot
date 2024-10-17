from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from callback_data.staff import PerformerRegisterCallbackData
from models import Performer
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

    def __init__(self, performer: Performer):
        self.__performer = performer

    def get_text(self) -> str:
        return (
            'Новый пользователь хочет зарегистрироваться\n'
            f'ФИО: {self.__performer.full_name}\n'
            'Номер телефона в каршеринге:'
            f' {self.__performer.car_sharing_phone_number}\n'
            'Номер телефона в компании Консоль:'
            f' {self.__performer.console_phone_number}\n'
        )

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        accept_button = InlineKeyboardButton(
            text='Подтвердить',
            callback_data=PerformerRegisterCallbackData(
                telegram_id=self.__performer.telegram_id,
            ).pack(),
        )
        reject_button = InlineKeyboardButton(
            text='Отклонить',
            callback_data='register-reject',
        )
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [reject_button],
                [accept_button],
            ],
        )

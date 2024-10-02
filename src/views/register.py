from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from views.base import TextView

__all__ = ('PerformerRegisterConfirmView',)


class PerformerRegisterConfirmView(TextView):

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

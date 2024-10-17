from collections.abc import Iterable

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from callback_data import CarWashDetailCallbackData
from callback_data.prefixes import CallbackDataPrefix
from models import CarWash
from views.base import TextView

__all__ = (
    'CarWashListView',
    'CarWashNameInputView',
    'CarWashCreateConfirmView',
)


class CarWashListView(TextView):

    def __init__(self, car_washes: Iterable[CarWash]):
        self.__car_washes = tuple(car_washes)

    def get_text(self) -> str:
        if not self.__car_washes:
            return 'Нет доступных моек'
        return 'Список моек'

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardBuilder()
        for car_wash in self.__car_washes:
            button = InlineKeyboardButton(
                text=car_wash.name,
                callback_data=CarWashDetailCallbackData(
                    car_wash_id=car_wash.id,
                ).pack(),
            )
            keyboard.row(button)

        car_wash_create_button = InlineKeyboardButton(
            text='Добавить мойку',
            callback_data=CallbackDataPrefix.CAR_WASH_CREATE,
        )
        keyboard.row(car_wash_create_button)
        return keyboard.as_markup()


class CarWashNameInputView(TextView):
    text = 'Введите название мойки'

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        back_button = InlineKeyboardButton(
            text='🔙 Назад',
            callback_data=CallbackDataPrefix.CAR_WASH_LIST,
        )
        return InlineKeyboardMarkup(inline_keyboard=[[back_button]])


class CarWashCreateConfirmView(TextView):
    reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='🔙 Назад',
                    callback_data=CallbackDataPrefix.CAR_WASH_CREATE,
                ),
                InlineKeyboardButton(
                    text='✅ Да',
                    callback_data=CallbackDataPrefix.CAR_WASH_CREATE_CONFIRM,
                ),
            ],
        ]
    )

    def __init__(self, car_wash_name: str):
        self.__car_wash_name = car_wash_name

    def get_text(self) -> str:
        return (
            f'❓ Вы уверены что хотите добавить мойку: {self.__car_wash_name}'
        )

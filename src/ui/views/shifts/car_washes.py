from collections.abc import Iterable

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from callback_data import (
    ShiftCarWashUpdateCallbackData,
    ShiftStartCarWashCallbackData,
)
from models import CarWash
from ui.views.base import TextView

__all__ = ('ShiftCarWashUpdateView', 'ShiftStartCarWashChooseView')


class ShiftCarWashUpdateView(TextView):
    text = 'Выберите мойку'

    def __init__(self, car_washes: Iterable[CarWash]):
        self.__car_washes = tuple(car_washes)

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardBuilder()
        keyboard.max_width = 1

        for car_wash in self.__car_washes:
            keyboard.button(
                text=car_wash.name,
                callback_data=ShiftCarWashUpdateCallbackData(
                    car_wash_id=car_wash.id,
                ),
            )

        return keyboard.as_markup()


class ShiftStartCarWashChooseView(TextView):
    text = '🚗 Для начала работы выберите мойку'

    def __init__(self, car_washes: Iterable[CarWash]):
        self.__car_washes = tuple(car_washes)

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardBuilder()
        keyboard.max_width = 1

        for car_wash in self.__car_washes:
            keyboard.button(
                text=car_wash.name,
                callback_data=ShiftStartCarWashCallbackData(
                    car_wash_id=car_wash.id,
                )
            )

        return keyboard.as_markup()

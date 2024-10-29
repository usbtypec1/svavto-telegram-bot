from collections.abc import Iterable

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from callback_data.prefixes import CallbackDataPrefix
from models import Car
from views.base import TextView

__all__ = ('CarsListView',)


class CarsListView(TextView):
    reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Главное меню',
                    callback_data=CallbackDataPrefix.STAFF_MENU,
                )
            ],
        ],
    )

    def __init__(self, cars: Iterable[Car]):
        self.__cars = tuple(cars)

    def get_text(self) -> str:
        if not self.__cars:
            return 'Вы пока не добавили ни одно авто'
        lines: list[str] = ['Добавленные авто за смену']

        for car in self.__cars:
            lines.append(f'📍 Гос.номер: {car.number}')

        return '\n'.join(lines)

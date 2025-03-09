from collections.abc import Iterable

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from callback_data.prefixes import CallbackDataPrefix
from ui.views import TextView


class DryCleaningCarNumberView(TextView):
    text = 'Выберите номер машины, для которой запрашиваете химчистку'

    def __init__(self, car_numbers: Iterable[str]):
        self.__car_numbers = tuple(car_numbers)

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardBuilder()

        for car_number in self.__car_numbers:
            keyboard.button(text=car_number, callback_data=car_number)

        keyboard.button(
            text='📝 Ввести вручную',
            callback_data=CallbackDataPrefix.CAR_NUMBER_INPUT,
        )

        return keyboard.as_markup()

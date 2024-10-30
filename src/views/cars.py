from collections.abc import Iterable

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, \
    ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

from callback_data import CarDetailForAdditionalServicesCallbackData
from callback_data.prefixes import CallbackDataPrefix
from models import Car
from views.base import TextView
from views.button_texts import ButtonText

__all__ = (
    'CarsListView',
    'CarsListForAdditionalServicesView',
    'CarAdditionalServicesUpdateView',
)


class CarsListForAdditionalServicesView(TextView):
    def __init__(self, cars: Iterable[Car]):
        self.__cars = tuple(cars)

    def get_text(self) -> str:
        if not self.__cars:
            return 'Вы пока не добавили ни одно авто за смену'
        return 'Выберите автомобиль из списка'

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardBuilder()
        keyboard.max_width = 1

        for car in self.__cars:
            keyboard.button(
                text=car.number,
                callback_data=CarDetailForAdditionalServicesCallbackData(
                    car_id=car.id,
                ),
            )

        return keyboard.as_markup()


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


class CarAdditionalServicesUpdateView(TextView):
    text = 'Нажмите кнопку ниже чтобы открыть меню выбора доп.услуг'

    def __init__(self, car_id: int, web_app_base_url: str):
        self.__car_id = car_id
        self.__web_app_base_url = web_app_base_url

    def get_reply_markup(self) -> ReplyKeyboardMarkup:
        button = KeyboardButton(
            text=ButtonText.CAR_ADDITIONAL_SERVICES,
            web_app=WebAppInfo(
                url=f'{self.__web_app_base_url}/shifts/cars/{self.__car_id}',
            )
        )
        return ReplyKeyboardMarkup(
            resize_keyboard=True,
            keyboard=[[button]],
        )

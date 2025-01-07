from collections.abc import Iterable

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

import ui.markups
import ui.buttons
from callback_data import CarWashActionCallbackData, CarWashDetailCallbackData
from callback_data.prefixes import CallbackDataPrefix
from enums import CarWashAction
from models import CarWash
from ui.views.base import TextView

__all__ = (
    'CarWashListView',
    'CarWashCreateNameInputView',
    'CarWashCreateConfirmView',
    'CarWashDetailView',
    'CarWashUpdateNameInputView',
    'CarWashRenameConfirmView',
    'CarWashDeleteConfirmView',
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


class CarWashCreateNameInputView(TextView):
    text = '✍️ Введите название мойки'

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        back_button = ui.buttons.create_back_button(
            callback_data=CallbackDataPrefix.CAR_WASH_LIST,
        )
        return InlineKeyboardMarkup(inline_keyboard=[[back_button]])


class CarWashUpdateNameInputView(TextView):
    text = '✍️ Введите название мойки'

    def __init__(self, car_wash_id: int):
        self.__car_wash_id = car_wash_id

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        back_button = ui.buttons.create_back_button(
            callback_data=CarWashDetailCallbackData(
                car_wash_id=self.__car_wash_id,
            ),
        )
        return InlineKeyboardMarkup(inline_keyboard=[[back_button]])


class CarWashCreateConfirmView(TextView):
    reply_markup = ui.markups.create_accept_and_back_markup(
        accept_callback_data=CallbackDataPrefix.CAR_WASH_CREATE_CONFIRM,
        back_callback_data=CallbackDataPrefix.CAR_WASH_CREATE,
    )

    def __init__(self, car_wash_name: str):
        self.__car_wash_name = car_wash_name

    def get_text(self) -> str:
        return (
            f'❓ Вы уверены что хотите добавить мойку: {self.__car_wash_name}'
        )


class CarWashDetailView(TextView):

    def __init__(self, car_wash: CarWash, web_app_base_url: str):
        self.__car_wash = car_wash
        self.__web_app_base_url = web_app_base_url

    def get_text(self) -> str:
        return (
            f'🆔 Мойка №{self.__car_wash.id}\n'
            f'🏷️ Название: {self.__car_wash.name}'
        )

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        car_washes_list_button = ui.buttons.create_back_button(
            callback_data=CallbackDataPrefix.CAR_WASH_LIST,
        )
        rename_button = InlineKeyboardButton(
            text='✏️ Переименовать',
            callback_data=CarWashActionCallbackData(
                car_wash_id=self.__car_wash.id,
                action=CarWashAction.RENAME,
            ).pack(),
        )
        price_list_button = InlineKeyboardButton(
            text='💰 Прайс-лист',
            web_app=WebAppInfo(
                url=f'{self.__web_app_base_url}/car-washes/'
                    f'{self.__car_wash.id}',
            ),
        )
        delete_button = InlineKeyboardButton(
            text='❌ Удалить',
            callback_data=CarWashActionCallbackData(
                car_wash_id=self.__car_wash.id,
                action=CarWashAction.DELETE,
            ).pack(),
        )
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [rename_button],
                [price_list_button],
                [delete_button],
                [car_washes_list_button],
            ]
        )


class CarWashRenameConfirmView(TextView):

    def __init__(self, *, car_wash_id: int, car_wash_name: str):
        """
        Keyword Args:
            car_wash_id: ID of car wash to rename.
            car_wash_name: New name of car wash.
        """
        self.__car_wash_id = car_wash_id
        self.__car_wash_name = car_wash_name

    def get_text(self) -> str:
        return (
            '❓ Вы уверены что хотите изменить название'
            f' мойки на: {self.__car_wash_name}'
        )

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        return ui.markups.create_accept_and_back_markup(
            accept_callback_data=CallbackDataPrefix.CAR_WASH_UPDATE_CONFIRM,
            back_callback_data=CarWashActionCallbackData(
                car_wash_id=self.__car_wash_id,
                action=CarWashAction.RENAME,
            ),
        )


class CarWashDeleteConfirmView(TextView):
    text = '❓ Вы уверены что хотите удалить мойку'

    def __init__(self, car_wash_id: int):
        self.__car_wash_id = car_wash_id

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        return ui.markups.create_accept_and_back_markup(
            accept_callback_data=CallbackDataPrefix.CAR_WASH_DELETE_CONFIRM,
            back_callback_data=CarWashDetailCallbackData(
                car_wash_id=self.__car_wash_id,
            ),
        )

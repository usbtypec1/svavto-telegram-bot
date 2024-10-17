from collections.abc import Iterable

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from callback_data import CarWashActionCallbackData, CarWashDetailCallbackData
from callback_data.prefixes import CallbackDataPrefix
from enums import CarWashAction
from models import CarWash
from views.base import TextView, ReplyMarkup

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
        back_button = InlineKeyboardButton(
            text='🔙 Назад',
            callback_data=CallbackDataPrefix.CAR_WASH_LIST,
        )
        return InlineKeyboardMarkup(inline_keyboard=[[back_button]])


class CarWashUpdateNameInputView(TextView):
    text = '✍️ Введите название мойки'

    def __init__(self, car_wash_id: int):
        self.__car_wash_id = car_wash_id

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        back_button = InlineKeyboardButton(
            text='🔙 Назад',
            callback_data=CarWashDetailCallbackData(
                car_wash_id=self.__car_wash_id,
            ).pack(),
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


class CarWashDetailView(TextView):

    def __init__(self, car_wash: CarWash):
        self.__car_wash = car_wash

    def get_text(self) -> str:
        return (
            f'🆔 Мойка №{self.__car_wash.id}\n'
            f'🏷️ Название: {self.__car_wash.name}'
        )

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        car_washes_list_button = InlineKeyboardButton(
            text='🔙 Назад',
            callback_data=CallbackDataPrefix.CAR_WASH_LIST,
        )
        rename_button = InlineKeyboardButton(
            text='✏️ Переименовать',
            callback_data=CarWashActionCallbackData(
                car_wash_id=self.__car_wash.id,
                action=CarWashAction.RENAME,
            ).pack(),
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
        back_button = InlineKeyboardButton(
            text='🔙 Назад',
            callback_data=CarWashActionCallbackData(
                car_wash_id=self.__car_wash_id,
                action=CarWashAction.RENAME,
            ).pack(),
        )
        confirm_button = InlineKeyboardButton(
            text='✅ Да',
            callback_data=CallbackDataPrefix.CAR_WASH_UPDATE_CONFIRM,
        )

        return InlineKeyboardMarkup(
            inline_keyboard=[
                [back_button, confirm_button],
            ],
        )


class CarWashDeleteConfirmView(TextView):
    text = '❓ Вы уверены что хотите удалить мойку'

    def __init__(self, car_wash_id: int):
        self.__car_wash_id = car_wash_id

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        back_button = InlineKeyboardButton(
            text='🔙 Назад',
            callback_data=CarWashDetailCallbackData(
                car_wash_id=self.__car_wash_id,
            ).pack(),
        )
        confirm_button = InlineKeyboardButton(
            text='✅ Да',
            callback_data=CallbackDataPrefix.CAR_WASH_DELETE_CONFIRM,
        )
        return InlineKeyboardMarkup(
            inline_keyboard=[[back_button, confirm_button]],
        )

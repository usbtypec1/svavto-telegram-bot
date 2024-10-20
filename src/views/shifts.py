from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from callback_data import (
    ShiftWorkTypeChoiceCallbackData,
    CarClassChoiceCallbackData,
    WashTypeChoiceCallbackData,
    WindshieldWasherRefilledValueCallbackData,
)
from callback_data.prefixes import CallbackDataPrefix
from enums import ShiftWorkType, CarClass, WashType
from views.base import TextView

__all__ = (
    'ShiftWorkTypeChoiceView',
    'shift_work_types_and_names',
    'CarNumberInputView',
    'CarClassInputView',
    'WashTypeInputView',
    'WindshieldWasherRefilledInputView',
    'WindshieldWasherRefilledValueInputView',
    'AdditionalServicesIncludedInputView',
    'AddCarWithoutAdditionalServicesConfirmView',
)

shift_work_types_and_names: tuple[tuple[ShiftWorkType, str], ...] = (
    (ShiftWorkType.MOVE_TO_WASH, 'Перегон ТС на мойку'),
    (ShiftWorkType.LIGHT_WASHES, 'Легкие мойки'),
    (ShiftWorkType.FIND_VEHICLE_IN_CITY, 'Поиск ТС в городе'),
    (ShiftWorkType.ASSIGNMENT_MOVE, 'Перегон по заданию'),
)


class ShiftWorkTypeChoiceView(TextView):
    text = 'Выберите направление, в котором хотите начать смену:'
    reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=shift_work_type_name,
                    callback_data=ShiftWorkTypeChoiceCallbackData(
                        work_type=shift_work_type,
                    ).pack(),
                )
            ]
            for shift_work_type, shift_work_type_name in
            shift_work_types_and_names
        ]
    )


class CarClassInputView(TextView):
    text = (
        'Укажите какому классу принадлежит автомобиль\n'
        '<blockquote expandable>'
        'Комфорт-класс: Volkswagen polo 6, skoda rapid 2,'
        ' chery tiggo 4, chery tiggo 4 pro, chery tiggo 7 pro ,'
        ' geely atlas pro, exeed lx, geely coolray, geely coolray flagship,'
        ' moskvich m3, nissan qashqai, renault duster, geely belgee x50'
        '\nБизнес-класс: audi a6, haval Jolion, Mercedes e200, Tank 300,'
        ' Tank 500, bmw 520d'
        '\nФургоны и микроавтобусы: ford transit, sollers atlant'
        '</blockquote>'
    )
    reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Комфорт',
                    callback_data=CarClassChoiceCallbackData(
                        car_class=CarClass.COMFORT,
                    ).pack(),
                ),
                InlineKeyboardButton(
                    text='Бизнес',
                    callback_data=CarClassChoiceCallbackData(
                        car_class=CarClass.BUSINESS,
                    ).pack(),
                ),
                InlineKeyboardButton(
                    text='Фургон',
                    callback_data=CarClassChoiceCallbackData(
                        car_class=CarClass.VAN,
                    ).pack(),
                ),
            ],
            [
                InlineKeyboardButton(
                    text='🔙 Назад',
                    callback_data=CallbackDataPrefix.CAR_NUMBER,
                )
            ]
        ]
    )


class CarNumberInputView(TextView):
    text = 'Укажите гос номер автомобиля в формате а111аа799'


class WashTypeInputView(TextView):
    text = 'Вид мойки'
    reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Плановая',
                    callback_data=WashTypeChoiceCallbackData(
                        wash_type=WashType.PLANNED,
                    ).pack(),
                ),
                InlineKeyboardButton(
                    text='Срочная',
                    callback_data=WashTypeChoiceCallbackData(
                        wash_type=WashType.URGENT,
                    ).pack(),
                ),
            ],
        ],
    )


class WindshieldWasherRefilledInputView(TextView):
    text = 'Осуществлен долив стеклоомывателя?'
    reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Да',
                    callback_data=(
                        CallbackDataPrefix.WINDSHIELD_WASHER_REFILLED_VALUE
                    ),
                ),
                InlineKeyboardButton(
                    text='Нет',
                    callback_data=WindshieldWasherRefilledValueCallbackData(
                        value=None,
                    ).pack(),
                ),
            ]
        ]
    )


windshield_washer_refilled_values: tuple[int, ...] = (
    10, 20, 30, 50, 70, 90, 100, 120,
)


class WindshieldWasherRefilledValueInputView(TextView):
    text = 'Сколько % от бутылки было залито?'

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardBuilder()
        keyboard.max_width = 2
        for value in windshield_washer_refilled_values:
            keyboard.button(
                text=f'{value}%',
                callback_data=WindshieldWasherRefilledValueCallbackData(
                    value=value,
                ).pack()
            )
        return keyboard.as_markup()


class AdditionalServicesIncludedInputView(TextView):
    text = 'Добавить доп услуги?'
    reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Да',
                    callback_data=(
                        CallbackDataPrefix.ADDITIONAL_SERVICES_INCLUDED
                    ),
                ),
                InlineKeyboardButton(
                    text='Добавить позже',
                    callback_data=CallbackDataPrefix.ADD_CAR_CONFIRM,
                ),
            ],
        ],
    )


class AddCarWithoutAdditionalServicesConfirmView(TextView):

    def __init__(self, car_number: str):
        self.__car_number = car_number

    def get_text(self) -> str:
        return (
            f'Автомобиль {self.__car_number} записан.'
            ' Добавить доп услуги или завершить автомобиль'
            ' можно будет позже в главном меню'
        )

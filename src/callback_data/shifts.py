from aiogram.filters.callback_data import CallbackData

from callback_data.prefixes import CallbackDataPrefix
from enums import ShiftWorkType, CarClass, WashType

__all__ = (
    'ShiftWorkTypeChoiceCallbackData',
    'CarClassChoiceCallbackData',
    'WashTypeChoiceCallbackData',
    'WindshieldWasherRefilledValueCallbackData',
)


class ShiftWorkTypeChoiceCallbackData(
    CallbackData,
    prefix=CallbackDataPrefix.SHIFT_WORK_TYPE,
):
    work_type: ShiftWorkType


class CarClassChoiceCallbackData(
    CallbackData,
    prefix=CallbackDataPrefix.CAR_CLASS,
):
    car_class: CarClass


class WashTypeChoiceCallbackData(
    CallbackData,
    prefix=CallbackDataPrefix.WASH_TYPE,
):
    wash_type: WashType


class WindshieldWasherRefilledValueCallbackData(
    CallbackData,
    prefix=CallbackDataPrefix.WINDSHIELD_WASHER_REFILLED_VALUE,
):
    value: int | None

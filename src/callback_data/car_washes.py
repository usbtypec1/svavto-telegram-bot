from aiogram.filters.callback_data import CallbackData

from callback_data.prefixes import CallbackDataPrefix

__all__ = ('CarWashDetailCallbackData', 'CarWashActionCallbackData')


class CarWashDetailCallbackData(
    CallbackData,
    prefix=CallbackDataPrefix.CAR_WASH_DETAIL,
):
    car_wash_id: int


class CarWashActionCallbackData(
    CallbackData,
    prefix=CallbackDataPrefix.CAR_WASH_UPDATE,
):
    car_wash_id: int
    action: str

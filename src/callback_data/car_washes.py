from aiogram.filters.callback_data import CallbackData

from callback_data.prefixes import CallbackDataPrefix

__all__ = ('CarWashDetailCallbackData',)


class CarWashDetailCallbackData(
    CallbackData,
    prefix=CallbackDataPrefix.CAR_WASH_DETAIL,
):
    car_wash_id: int

from aiogram.filters.callback_data import CallbackData

from callback_data.prefixes import CallbackDataPrefix

__all__ = ('CarDetailForAdditionalServicesCallbackData',)


class CarDetailForAdditionalServicesCallbackData(
    CallbackData,
    prefix=CallbackDataPrefix.CAR_DETAIL_FOR_ADDITIONAL_SERVICES,
):
    car_id: int

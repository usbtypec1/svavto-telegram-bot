from aiogram import F, Router
from aiogram.filters import StateFilter, invert_f
from aiogram.types import CallbackQuery, Message
from fast_depends import Depends, inject

from callback_data import CarDetailForAdditionalServicesCallbackData
from config import Config
from dependencies.repositories import get_car_to_wash_repository
from filters import admins_filter
from models import CarAdditionalServices
from repositories import CarToWashRepository
from views.base import answer_view
from views.button_texts import ButtonText
from views.cars import (
    CarAdditionalServicesUpdateView,
    CarsListForAdditionalServicesView,
)

__all__ = ('router',)

from views.menu import ShiftMenuView

router = Router(name=__name__)


@router.message(
    F.web_app_data.button_text == ButtonText.CAR_ADDITIONAL_SERVICES,
    invert_f(admins_filter),
    StateFilter('*'),
)
@inject
async def on_car_additional_services_edit(
        message: Message,
        config: Config,
        car_to_wash_repository: CarToWashRepository = Depends(
            dependency=get_car_to_wash_repository,
            use_cache=False,
        ),
):
    car_additional_services = CarAdditionalServices.model_validate_json(
        message.web_app_data.data,
    )
    await car_to_wash_repository.update_additional_services(
        car_additional_services,
    )
    await message.answer('Доп.услуги машины обновлены')
    view = ShiftMenuView(
        staff_id=message.from_user.id,
        web_app_base_url=config.web_app_base_url,
    )
    await answer_view(message, view)


@router.callback_query(
    CarDetailForAdditionalServicesCallbackData.filter(),
    invert_f(admins_filter),
    StateFilter('*'),
)
async def on_shift_added_car_additional_services_edit(
        callback_query: CallbackQuery,
        callback_data: CarDetailForAdditionalServicesCallbackData,
        config: Config,
) -> None:
    view = CarAdditionalServicesUpdateView(
        car_id=callback_data.car_id,
        web_app_base_url=config.web_app_base_url,
    )
    await answer_view(callback_query.message, view)


@router.message(
    F.text == ButtonText.SHIFT_ADDITIONAL_SERVICES,
    invert_f(admins_filter),
    StateFilter('*'),
)
@inject
async def on_shift_added_cars_list(
        message: Message,
        car_to_wash_repository: CarToWashRepository = Depends(
            dependency=get_car_to_wash_repository,
            use_cache=False,
        ),
) -> None:
    cars = await car_to_wash_repository.get_all(message.from_user.id)
    view = CarsListForAdditionalServicesView(cars)
    await answer_view(message, view)

from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.types import Message
from fast_depends import Depends, inject

from config import Config
from dependencies.repositories import get_car_to_wash_repository
from filters import admins_filter
from repositories import CarToWashRepository
from services.shifts import get_current_shift_date
from views.base import answer_text_view
from views.button_texts import ButtonText
from views.shifts import (
    ShiftCarsCountByStaffView,
    ShiftCarsWithoutWindshieldWasherView,
)

__all__ = ('router',)

router = Router(name=__name__)


@router.message(
    F.text == ButtonText.SHIFT_CARS_COUNT_BY_STAFF,
    admins_filter,
    StateFilter('*')
)
@inject
async def on_show_shift_cars_count_by_staff(
        message: Message,
        config: Config,
        car_to_wash_repository: CarToWashRepository = Depends(
            get_car_to_wash_repository,
            use_cache=False,
        ),
) -> None:
    shift_date = get_current_shift_date(config.timezone)
    shift_cars = await car_to_wash_repository.get_count_by_staff(shift_date)
    view = ShiftCarsCountByStaffView(shift_cars)
    await answer_text_view(message, view)


@router.message(
    F.text == ButtonText.SHIFT_CARS_WITHOUT_WINDSHIELD_WASHER,
    admins_filter,
    StateFilter('*')
)
@inject
async def on_show_shift_cars_without_windshield_washer(
        message: Message,
        config: Config,
        car_to_wash_repository: CarToWashRepository = Depends(
            get_car_to_wash_repository,
            use_cache=False,
        ),
) -> None:
    shift_date = get_current_shift_date(config.timezone)
    shift_cars = await car_to_wash_repository.get_without_windshield_washer(
        shift_date,
    )
    view = ShiftCarsWithoutWindshieldWasherView(shift_cars)
    await answer_text_view(message, view)

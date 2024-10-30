from datetime import datetime
from zoneinfo import ZoneInfo

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import Message
from fast_depends import inject, Depends

from config import Config
from dependencies.repositories import get_car_to_wash_repository
from filters import admins_filter
from repositories import CarToWashRepository
from views.base import answer_view
from views.button_texts import ButtonText
from views.shifts import ShiftCarsCountByStaffView, \
    ShiftCarsWithoutWindshieldWasherView

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
    now = datetime.now(ZoneInfo(config.timezone))
    shift_cars = await car_to_wash_repository.get_count_by_staff(now)
    view = ShiftCarsCountByStaffView(shift_cars)
    await answer_view(message, view)


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
    now = datetime.now(ZoneInfo(config.timezone))
    shift_cars = await car_to_wash_repository.get_without_windshield_washer(now)
    view = ShiftCarsWithoutWindshieldWasherView(shift_cars)
    await answer_view(message, view)

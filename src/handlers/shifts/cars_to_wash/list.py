from aiogram import Router, F
from aiogram.filters import StateFilter, invert_f
from aiogram.types import Message
from fast_depends import Depends, inject

from dependencies.repositories import get_car_to_wash_repository
from filters import admins_filter
from repositories import CarToWashRepository
from views.base import answer_text_view
from views.button_texts import ButtonText
from views.cars import CarsListView

__all__ = ('router',)

router = Router(name=__name__)


@router.message(
    F.text == ButtonText.SHIFT_ADDED_CARS,
    invert_f(admins_filter),
    StateFilter('*'),
)
@inject
async def on_show_cars_added_on_shift(
        message: Message,
        car_to_wash_repository: CarToWashRepository = Depends(
            dependency=get_car_to_wash_repository,
            use_cache=False,
        ),
) -> None:
    cars = await car_to_wash_repository.get_all(message.from_user.id)
    view = CarsListView(cars)
    await answer_text_view(message, view)

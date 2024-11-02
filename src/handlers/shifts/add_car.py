from aiogram import F, Router
from aiogram.filters import StateFilter, invert_f
from aiogram.types import Message
from fast_depends import Depends, inject

from dependencies.repositories import get_car_to_wash_repository
from filters import admins_filter
from models import CarToWash
from repositories import CarToWashRepository
from views.button_texts import ButtonText

__all__ = ('router',)

router = Router(name=__name__)


@router.message(
    F.web_app_data.button_text == ButtonText.SHIFT_ADD_CAR,
    invert_f(admins_filter),
    StateFilter('*'),
)
@inject
async def on_input_car(
        message: Message,
        car_to_wash_repository: CarToWashRepository = Depends(
            dependency=get_car_to_wash_repository,
            use_cache=False,
        ),
) -> None:
    car_to_wash = CarToWash.model_validate(message.web_app_data.data)
    await car_to_wash_repository.create(car_to_wash)

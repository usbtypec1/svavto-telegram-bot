from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.types import Message
from fast_depends import inject

from config import Config
from dependencies.repositories import CarToWashRepositoryDependency
from filters import admins_filter
from services.shifts import get_current_shift_date
from ui.views import (
    answer_text_view, ButtonText,
)
from ui.views.supervision import SupervisionTransferredCarsView


__all__ = ('router',)

router = Router(name=__name__)


@router.message(
    F.text == ButtonText.SUPERVISION_CAR_TRANSFERS,
    admins_filter,
    StateFilter('*')
)
@inject
async def on_show_shift_cars_count_by_staff(
        message: Message,
        config: Config,
        car_to_wash_repository: CarToWashRepositoryDependency,
) -> None:
    shift_date = get_current_shift_date(config.timezone)
    shift_cars = await car_to_wash_repository.get_count_by_staff(shift_date)
    view = SupervisionTransferredCarsView(shift_cars)
    await answer_text_view(message, view)

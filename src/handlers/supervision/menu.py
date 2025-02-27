from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.types import Message
from fast_depends import inject

from config import Config
from dependencies.repositories import (
    CarToWashRepositoryDependency,
)
from filters import admins_filter
from services.shifts import get_current_shift_date
from ui.views import (
    answer_text_view, ButtonText,
)
from ui.views.supervision.windshield_washer import \
    SupervisionWindshieldWasherView
from ui.views.supervision.menu import SupervisionMenuView


__all__ = ('router',)

router = Router(name=__name__)


@router.message(
    F.text == ButtonText.SUPERVISION_MENU,
    admins_filter,
    StateFilter('*')
)
async def on_show_supervision_menu(message: Message) -> None:
    await answer_text_view(message, SupervisionMenuView())


@router.message(
    F.text == ButtonText.SHIFT_CARS_WITHOUT_WINDSHIELD_WASHER,
    admins_filter,
    StateFilter('*')
)
@inject
async def on_show_shift_cars_without_windshield_washer(
        message: Message,
        config: Config,
        car_to_wash_repository: CarToWashRepositoryDependency,
) -> None:
    shift_date = get_current_shift_date(config.timezone)
    shift_cars = await car_to_wash_repository.get_without_windshield_washer(
        shift_date,
    )
    view = SupervisionWindshieldWasherView(shift_cars)
    await answer_text_view(message, view)

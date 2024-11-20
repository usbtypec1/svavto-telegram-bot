from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery
from fast_depends import inject, Depends

from callback_data import CarWashDetailCallbackData
from config import Config
from dependencies.repositories import get_car_wash_repository
from filters import admins_filter
from repositories import CarWashRepository
from views.base import edit_message_by_view
from views.car_washes import CarWashDetailView

__all__ = ('router',)

router = Router(name=__name__)


@router.callback_query(
    CarWashDetailCallbackData.filter(),
    admins_filter,
    StateFilter('*'),
)
@inject
async def on_show_car_wash_detail(
        callback_query: CallbackQuery,
        callback_data: CarWashDetailCallbackData,
        config: Config,
        car_wash_repository: CarWashRepository = Depends(
            dependency=get_car_wash_repository,
            use_cache=False,
        ),
) -> None:
    car_wash = await car_wash_repository.get_by_id(callback_data.car_wash_id)
    view = CarWashDetailView(car_wash, config.web_app_base_url)
    await edit_message_by_view(callback_query.message, view)

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery
from fast_depends import Depends, inject

from callback_data.prefixes import CallbackDataPrefix
from dependencies.repositories import get_car_wash_repository
from filters import admins_filter
from repositories import CarWashRepository
from ui.views import answer_text_view, edit_message_by_view
from ui.views import ButtonText
from ui.views import CarWashListView

__all__ = ('router',)

router = Router(name=__name__)


@router.message(
    F.text == ButtonText.CAR_WASH_LIST,
    admins_filter,
    StateFilter('*'),
)
@router.callback_query(
    F.data == CallbackDataPrefix.CAR_WASH_LIST,
    admins_filter,
    StateFilter('*'),
)
@inject
async def on_show_car_washes_list(
        message_or_callback_query: Message | CallbackQuery,
        car_wash_repository: CarWashRepository = Depends(
            dependency=get_car_wash_repository,
            use_cache=False,
        ),
) -> None:
    car_washes = await car_wash_repository.get_all()
    view = CarWashListView(car_washes)
    if isinstance(message_or_callback_query, Message):
        await answer_text_view(message_or_callback_query, view)
    else:
        await edit_message_by_view(message_or_callback_query.message, view)

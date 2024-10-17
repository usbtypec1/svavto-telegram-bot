from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.types import Message

from filters import admins_filter

__all__ = ('router',)

router = Router(name=__name__)


@router.message(
    admins_filter,
    StateFilter('*'),
)
async def on_show_car_washes_list(
        message: Message,
) -> None:
    pass

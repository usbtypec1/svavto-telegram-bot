from aiogram import Router
from aiogram.filters import StateFilter, Command, invert_f
from aiogram.types import Message

from filters import admins_filter
from views.base import answer_view
from views.menu import StaffShiftCarWashMenuView

__all__ = ('router',)

router = Router(name=__name__)


@router.message(
    Command('shift'),
    invert_f(admins_filter),
    StateFilter('*'),
)
async def on_show_staff_shift_car_wash_menu(
        message: Message,
) -> None:
    view = StaffShiftCarWashMenuView()
    await answer_view(message, view)

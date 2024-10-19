from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import Message

from views.base import answer_view
from views.button_texts import ButtonText
from views.schedules import StaffScheduleMenu

__all__ = ('router',)

router = Router(name=__name__)


@router.message(
    F.text == ButtonText.SHIFT_SCHEDULE,
    StateFilter('*'),
)
async def on_show_shift_schedule_menu(message: Message) -> None:
    await answer_view(message, StaffScheduleMenu())

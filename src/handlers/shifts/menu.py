from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.types import Message

from config import Config
from filters import staff_filter
from ui.views import answer_text_view, ShiftMenuView

__all__ = ('router',)

router = Router(name=__name__)


@router.message(
    Command('shift'),
    staff_filter,
    StateFilter('*'),
)
async def on_show_staff_shift_car_wash_menu(
        message: Message,
        config: Config,
) -> None:
    view = ShiftMenuView(
        staff_id=message.from_user.id,
        web_app_base_url=config.web_app_base_url,
    )
    await answer_text_view(message, view)

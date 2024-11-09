from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.types import Message

from config import Config
from filters import admins_filter
from views.admins import AdminShiftsMenuView
from views.base import answer_view
from views.button_texts import ButtonText

__all__ = ('router',)

router = Router(name=__name__)


@router.message(
    F.text == ButtonText.SHIFTS,
    admins_filter,
    StateFilter('*'),
)
async def on_show_staff_list(
        message: Message,
        config: Config,
) -> None:
    view = AdminShiftsMenuView(config.web_app_base_url)
    await answer_view(message, view)

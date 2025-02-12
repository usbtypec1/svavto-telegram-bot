from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.types import Message

from config import Config
from filters import admins_filter
from ui.views import answer_text_view, ButtonText, PenaltyCreateMenuView

__all__ = ('router',)

router = Router(name=__name__)


@router.message(
    F.text == ButtonText.PENALTY_CREATE_MENU,
    admins_filter,
    StateFilter('*'),
)
async def on_show_penalty_create_menu(
        message: Message,
        config: Config,
) -> None:
    view = PenaltyCreateMenuView(web_app_base_url=config.web_app_base_url)
    await answer_text_view(message, view)

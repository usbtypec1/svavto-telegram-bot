from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.types import Message

from config import Config
from filters import admins_filter
from ui.views import answer_text_view, ButtonText, SurchargeCreateMenuView


__all__ = ('router',)

router = Router(name=__name__)


@router.message(
    F.text == ButtonText.SURCHARGE_CREATE_MENU,
    admins_filter,
    StateFilter('*'),
)
async def on_show_surcharge_create_menu(
        message: Message,
        config: Config,
) -> None:
    view = SurchargeCreateMenuView(web_app_base_url=config.web_app_base_url)
    await answer_text_view(message, view)

from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.types import Message

from config import Config
from filters import admins_filter
from ui.views import AdminShiftsMenuView
from ui.views import answer_text_view
from ui.views import ButtonText

__all__ = ('router',)

router = Router(name=__name__)


@router.message(
    F.text == ButtonText.SHIFTS_ADMIN_MENU,
    admins_filter,
    StateFilter('*'),
)
async def on_show_staff_list(
        message: Message,
        config: Config,
) -> None:
    view = AdminShiftsMenuView(
        web_app_base_url=config.web_app_base_url,
        shifts_table_url=config.shifts_table_url,
    )
    await answer_text_view(message, view)

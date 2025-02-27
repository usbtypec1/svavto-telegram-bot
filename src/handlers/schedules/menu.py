from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import Message

from config import Config
from ui.views import answer_text_view
from ui.views import ButtonText
from ui.views import StaffShiftsScheduleMenuView

__all__ = ('router',)

router = Router(name=__name__)


@router.message(
    F.text == ButtonText.SHIFT_SCHEDULE,
    StateFilter('*'),
)
async def on_show_shift_schedule_menu(
        message: Message,
        config: Config,
) -> None:
    await answer_text_view(message, StaffShiftsScheduleMenuView(config.web_app_base_url))

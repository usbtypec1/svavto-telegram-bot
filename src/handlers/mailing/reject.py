from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from callback_data.prefixes import CallbackDataPrefix
from config import Config
from filters import admins_filter
from states import MailingStates
from ui.views import AdminMenuView, edit_as_rejected
from ui.views import answer_text_view

__all__ = ('router',)

router = Router(name=__name__)


@router.callback_query(
    F.data == CallbackDataPrefix.MAILING_CREATE_REJECT,
    admins_filter,
    StateFilter(MailingStates.confirm)
)
async def on_reject_mailing(
        callback_query: CallbackQuery,
        state: FSMContext,
        config: Config,
) -> None:
    await state.clear()
    await edit_as_rejected(callback_query.message)
    view = AdminMenuView(config.web_app_base_url)
    await answer_text_view(callback_query.message, view)

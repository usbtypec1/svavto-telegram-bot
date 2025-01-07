from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from config import Config
from enums import MailingType
from filters import admins_filter
from states import MailingStates
from ui.views import answer_text_view
from ui.views import ButtonText
from ui.views import (
    MailingPhotoInputView,
    MailingStaffWebAppView,
    MailingTextInputView,
)

__all__ = ('router',)

router = Router(name=__name__)


@router.message(
    admins_filter,
    F.text,
    StateFilter(MailingStates.text)
)
async def on_input_text(
        message: Message,
        state: FSMContext,
        config: Config,
) -> None:
    await state.update_data(text=message.html_text)
    state_data: dict = await state.get_data()
    mailing_type: MailingType = state_data['type']
    if mailing_type == MailingType.SPECIFIC_STAFF:
        await state.set_state(MailingStates.chat_ids)
        view = MailingStaffWebAppView(config.web_app_base_url)
    else:
        await state.set_state(MailingStates.photos)
        view = MailingPhotoInputView()
    await answer_text_view(message, view)


@router.callback_query(
    F.text == ButtonText.MAILING,
    admins_filter,
    StateFilter('*'),
)
async def on_start_mailing_to_all_flow(
        callback_query: CallbackQuery,
        state: FSMContext,
) -> None:
    await state.set_state(MailingStates.text)
    view = MailingTextInputView()
    await answer_text_view(callback_query.message, view)

import json

from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from filters import admins_filter
from states import MailingStates
from views.base import answer_view
from views.button_texts import ButtonText
from views.mailing import MailingPhotoInputView

__all__ = ('router',)

router = Router(name=__name__)


@router.message(
    F.web_app_data.button_text == ButtonText.MAILING_STAFF,
    admins_filter,
    StateFilter(MailingStates.chat_ids),
)
async def on_show_chat_ids(
        message: Message,
        state: FSMContext,
) -> None:
    chat_ids: list[int] = json.loads(message.web_app_data.data)
    await state.update_data(chat_ids=chat_ids)
    await state.set_state(MailingStates.photos)
    view = MailingPhotoInputView()
    await answer_view(message, view)

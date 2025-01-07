from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from filters import admins_filter
from models import MailingParams
from services.mailing import render_message_for_mailing
from services.telegram_events import parse_web_app_data_buttons
from states import MailingStates
from views.base import answer_text_view
from views.button_texts import ButtonText
from views.mailing import MailingConfirmView

__all__ = ('router',)

router = Router(name=__name__)


@router.message(
    F.text == ButtonText.SKIP,
    admins_filter,
    StateFilter(MailingStates.reply_markup)
)
async def on_skip_reply_markup(
        message: Message,
        state: FSMContext,
) -> None:
    state_data: dict = await state.get_data()
    mailing_params = MailingParams.model_validate(state_data)
    await render_message_for_mailing(
        message=message,
        text=mailing_params.text,
        photo_file_ids=mailing_params.photo_file_ids,
        reply_markup=None,
    )

    await state.update_data(reply_markup=None)
    await state.set_state(MailingStates.confirm)
    view = MailingConfirmView()
    await answer_text_view(message, view)


@router.message(
    F.web_app_data.button_text == ButtonText.ATTACH_REPLY_MARKUP,
    admins_filter,
    StateFilter(MailingStates.reply_markup)
)
async def on_input_reply_markup(
        message: Message,
        state: FSMContext,
) -> None:
    state_data: dict = await state.get_data()
    markup = parse_web_app_data_buttons(message.web_app_data.data)
    mailing_params = MailingParams.model_validate(state_data)
    await render_message_for_mailing(
        message=message,
        text=mailing_params.text,
        photo_file_ids=mailing_params.photo_file_ids,
        reply_markup=markup,
    )
    await state.update_data(reply_markup=markup.model_dump_json())
    await state.set_state(MailingStates.confirm)
    view = MailingConfirmView()
    await answer_text_view(message, view)

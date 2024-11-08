from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramConflictError
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from filters import admins_filter
from services.telegram_events import (
    parse_web_app_data_buttons,
    reply_markup_to_buttons,
)
from states import MailingStates, MailingToLastActiveStaffStates
from views.base import answer_view
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
    text: str = state_data['text']
    await message.answer(
        text=text,
        parse_mode=ParseMode.HTML,
    )
    await state.update_data(reply_markup=None)
    await state.set_state(MailingToLastActiveStaffStates.confirm)
    view = MailingConfirmView()
    await answer_view(message, view)


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
    try:
        await message.answer(
            text=state_data['text'],
            reply_markup=markup,
            parse_mode=ParseMode.HTML,
        )
    except TelegramConflictError:
        await message.answer('Неправильный формат текста или кнопок')
        return
    await state.update_data(reply_markup=markup.model_dump_json())
    await state.set_state(MailingToLastActiveStaffStates.confirm)
    view = MailingConfirmView()
    await answer_view(message, view)

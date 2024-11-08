from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from callback_data import MailingTypeChooseCallbackData
from filters import admins_filter
from states import MailingStates
from views.base import answer_view, edit_message_by_view
from views.button_texts import ButtonText
from views.mailing import MailingTextInputView, MailingTypeChooseView

__all__ = ('router',)

router = Router(name=__name__)


@router.callback_query(
    MailingTypeChooseCallbackData.filter(),
    admins_filter,
    StateFilter(MailingStates.type),
)
async def on_choose_mailing_type(
        callback_query: CallbackQuery,
        callback_data: MailingTypeChooseCallbackData,
        state: FSMContext,
) -> None:
    await state.update_data(type=callback_data.type)
    await state.set_state(MailingStates.text)
    view = MailingTextInputView()
    await edit_message_by_view(callback_query.message, view)
    await callback_query.answer()


@router.message(
    F.text == ButtonText.MAILING,
    admins_filter,
    StateFilter('*'),
)
async def on_show_mailing_types(
        message: Message,
        state: FSMContext,
) -> None:
    view = MailingTypeChooseView()
    await state.set_state(MailingStates.type)
    await answer_view(message, view)

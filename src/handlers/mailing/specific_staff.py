from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramConflictError
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from fast_depends import Depends, inject

from callback_data import MailingTypeChooseCallbackData
from callback_data.prefixes import CallbackDataPrefix
from config import Config
from dependencies.repositories import get_mailing_repository
from enums import MailingType
from filters import admins_filter
from repositories.mailing import MailingRepository
from services.telegram_events import (
    parse_web_app_data_buttons,
    parse_chat_ids_json,
)
from states import MailingToSpecificStaffStates
from views.admins import AdminMenuView
from views.base import answer_view
from views.button_texts import ButtonText
from views.mailing import (
    MailingTextInputView,
    MailingReplyMarkupWebAppView,
    MailingConfirmView,
    MailingStaffWebAppView,
)

__all__ = ('router',)

router = Router(name=__name__)


@router.callback_query(
    F.data == CallbackDataPrefix.MAILING_CREATE_REJECT,
    admins_filter,
    StateFilter(MailingToSpecificStaffStates.confirm)
)
async def on_reject_mailing(
        callback_query: CallbackQuery,
        state: FSMContext,
) -> None:
    await state.clear()
    await callback_query.message.edit_text(
        f'{callback_query.message.text}\n\n<i>Отменено</i>',
    )
    view = AdminMenuView()
    await answer_view(callback_query.message, view)


@router.callback_query(
    F.data == CallbackDataPrefix.MAILING_CREATE_ACCEPT,
    admins_filter,
    StateFilter(MailingToSpecificStaffStates.confirm)
)
@inject
async def on_confirm_mailing(
        callback_query: CallbackQuery,
        state: FSMContext,
        mailing_repository: MailingRepository = Depends(
            dependency=get_mailing_repository,
            use_cache=False,
        ),
) -> None:
    state_data: dict = await state.get_data()
    await state.clear()
    text: str = state_data['text']
    reply_markup: str | None = state_data['reply_markup']
    chat_ids: list[int] = state_data['chat_ids']
    await mailing_repository.send_to_specific_staff(
        text=text,
        reply_markup=reply_markup,
        chat_ids=chat_ids,
    )
    await callback_query.answer('Рассылка создана', show_alert=True)
    await callback_query.message.delete_reply_markup()
    view = AdminMenuView()
    await answer_view(callback_query.message, view)


@router.message(
    F.text == ButtonText.SKIP,
    admins_filter,
    StateFilter(MailingToSpecificStaffStates.reply_markup)
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
    await state.set_state(MailingToSpecificStaffStates.confirm)
    view = MailingConfirmView()
    await answer_view(message, view)


@router.message(
    F.web_app_data.button_text == ButtonText.ATTACH_REPLY_MARKUP,
    admins_filter,
    StateFilter(MailingToSpecificStaffStates.reply_markup)
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
    await state.update_data(reply_markup=message.web_app_data.data)
    await state.set_state(MailingToSpecificStaffStates.confirm)
    view = MailingConfirmView()
    await answer_view(message, view)


@router.message(
    F.web_app_data.button_text == ButtonText.MAILING_STAFF,
    admins_filter,
    StateFilter(MailingToSpecificStaffStates.chat_ids)
)
async def on_staff_chosen(
        message: Message,
        state: FSMContext,
        config: Config,
) -> None:
    chat_ids = parse_chat_ids_json(message.web_app_data.data)
    await state.update_data(chat_ids=chat_ids)
    await state.set_state(MailingToSpecificStaffStates.reply_markup)
    view = MailingReplyMarkupWebAppView(config.web_app_base_url)
    await answer_view(message, view)


@router.message(
    admins_filter,
    F.text,
    StateFilter(MailingToSpecificStaffStates.text)
)
async def on_input_text(
        message: Message,
        state: FSMContext,
        config: Config,
) -> None:
    await state.update_data(text=message.html_text)
    await state.set_state(MailingToSpecificStaffStates.chat_ids)
    view = MailingStaffWebAppView(config.web_app_base_url)
    await answer_view(message, view)


@router.callback_query(
    MailingTypeChooseCallbackData.filter(F.type == MailingType.SPECIFIC_STAFF),
    admins_filter,
    StateFilter('*'),
)
async def on_start_mailing_to_specific_staff_flow(
        callback_query: CallbackQuery,
        state: FSMContext,
) -> None:
    await state.set_state(MailingToSpecificStaffStates.text)
    view = MailingTextInputView()
    await answer_view(callback_query.message, view)

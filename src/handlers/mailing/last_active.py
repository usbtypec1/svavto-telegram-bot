from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramConflictError
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup
from fast_depends import Depends, inject

from callback_data import MailingTypeChooseCallbackData
from callback_data.prefixes import CallbackDataPrefix
from config import Config
from dependencies.repositories import get_mailing_repository
from enums import MailingType
from filters import admins_filter
from models import Button
from repositories.mailing import MailingRepository
from services.telegram_events import parse_web_app_data_buttons, \
    reply_markup_to_buttons
from states.mailing import MailingToLastActiveStaffStates
from views.admins import AdminMenuView
from views.base import answer_view
from views.button_texts import ButtonText
from views.mailing import (
    MailingTextInputView,
    MailingReplyMarkupWebAppView,
    MailingConfirmView,
)

__all__ = ('router',)

router = Router(name=__name__)


@router.callback_query(
    F.data == CallbackDataPrefix.MAILING_CREATE_REJECT,
    admins_filter,
    StateFilter(MailingToLastActiveStaffStates.confirm)
)
async def on_reject_mailing(
        callback_query: CallbackQuery,
        state: FSMContext,
) -> None:
    await state.clear()
    await callback_query.message.edit_text(
        f'{callback_query.message.text}\n\n<i>Отменено</i>'
    )
    view = AdminMenuView()
    await answer_view(callback_query.message, view)


@router.callback_query(
    F.data == CallbackDataPrefix.MAILING_CREATE_ACCEPT,
    admins_filter,
    StateFilter(MailingToLastActiveStaffStates.confirm)
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
    reply_markup: list[list[Button]] | None = state_data['reply_markup']
    await mailing_repository.send_to_last_active_staff(
        text=text,
        reply_markup=reply_markup,
        last_days=30,
    )
    await callback_query.answer('Рассылка создана', show_alert=True)
    await callback_query.message.delete_reply_markup()
    view = AdminMenuView()
    await answer_view(callback_query.message, view)


@router.message(
    F.text == ButtonText.SKIP,
    admins_filter,
    StateFilter(MailingToLastActiveStaffStates.reply_markup)
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
    StateFilter(MailingToLastActiveStaffStates.reply_markup)
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
    await state.update_data(reply_markup=reply_markup_to_buttons(markup))
    await state.set_state(MailingToLastActiveStaffStates.confirm)
    view = MailingConfirmView()
    await answer_view(message, view)


@router.message(
    admins_filter,
    F.text,
    StateFilter(MailingToLastActiveStaffStates.text)
)
async def on_input_text(
        message: Message,
        state: FSMContext,
        config: Config,
) -> None:
    await state.update_data(text=message.html_text)
    await state.set_state(MailingToLastActiveStaffStates.reply_markup)
    view = MailingReplyMarkupWebAppView(config.web_app_base_url)
    await answer_view(message, view)


@router.callback_query(
    MailingTypeChooseCallbackData.filter(F.type == MailingType.LAST_ACTIVE),
    admins_filter,
    StateFilter('*'),
)
async def on_start_mailing_to_all_flow(
        callback_query: CallbackQuery,
        state: FSMContext,
) -> None:
    await state.set_state(MailingToLastActiveStaffStates.text)
    view = MailingTextInputView()
    await answer_view(callback_query.message, view)

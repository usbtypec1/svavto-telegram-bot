from aiogram import Bot, F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from callback_data.prefixes import CallbackDataPrefix
from config import Config
from filters import admins_filter
from states import MailingStates
from ui.views import answer_text_view
from ui.views import (
    MailingConfirmView,
    MailingPhotoAcceptedView,
    MailingPhotoAlreadyAcceptedView,
    MailingReplyMarkupWebAppView,
)

__all__ = ('router',)

router = Router(name=__name__)


@router.callback_query(
    F.data == CallbackDataPrefix.MAILING_PHOTO_ACCEPT_FINISH,
    admins_filter,
    StateFilter(MailingStates.photos)
)
async def on_mailing_photo_accept_finish(
        callback_query: CallbackQuery,
        state: FSMContext,
        config: Config,
        bot: Bot,
) -> None:
    state_data: dict = await state.get_data()
    photo_file_ids: list[str] = state_data.get('photo_file_ids', [])
    message_ids_to_remove: list[int] = state_data.get(
        'message_ids_to_remove',
        [],
    )
    if len(photo_file_ids) > 1:
        await callback_query.message.answer(
            '❗️ Так как вы выбрали несколько фотографий,'
            ' то вы не сможете прикрепить кнопки'
        )
        await state.set_state(MailingStates.confirm)
        view = MailingConfirmView()
    else:
        await state.set_state(MailingStates.reply_markup)
        view = MailingReplyMarkupWebAppView(config.web_app_base_url)
    await answer_text_view(callback_query.message, view)

    if message_ids_to_remove:
        await bot.delete_messages(
            chat_id=callback_query.message.chat.id,
            message_ids=message_ids_to_remove,
        )


@router.message(
    F.photos,
    admins_filter,
    StateFilter(MailingStates.photos)
)
async def on_input_photo(
        message: Message,
        state: FSMContext,
) -> None:
    file_id = message.photo[-1].file_id
    state_data = await state.get_data()
    photo_file_ids: list[str] = state_data.get('photo_file_ids', [])
    message_ids_to_remove: list[int] = state_data.get(
        'message_ids_to_remove',
        [],
    )
    if file_id not in photo_file_ids:
        photo_file_ids.append(file_id)
        view = MailingPhotoAcceptedView()
    else:
        view = MailingPhotoAlreadyAcceptedView()
    sent_message = await answer_text_view(message, view)
    message_ids_to_remove.append(sent_message.message_id)
    await state.update_data(
        photo_file_ids=photo_file_ids,
        message_ids_to_remove=message_ids_to_remove,
    )

from aiogram import F, Router
from aiogram.filters import StateFilter, invert_f
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from fast_depends import Depends, inject

from callback_data.prefixes import CallbackDataPrefix
from config import Config
from dependencies.repositories import get_shift_repository
from filters import admins_filter
from repositories import ShiftRepository
from services.notifications import SpecificChatsNotificationService
from services.telegram_events import format_accept_text, format_reject_text
from states import ShiftFinishStates
from views.base import answer_media_group_view, answer_view
from views.button_texts import ButtonText
from views.menu import MainMenuView, ShiftMenuView
from views.shifts import (
    ShiftFinishConfirmAllView,
    ShiftFinishConfirmView,
    ShiftFinishPhotoConfirmView,
    ShiftFinishPhotosView, StaffFirstShiftFinishedView,
    StaffShiftFinishedNotificationView, StaffShiftFinishedView,
)

__all__ = ('router',)

router = Router(name=__name__)


@router.message(
    F.text == ButtonText.LATER,
    invert_f(admins_filter),
    StateFilter('*'),
)
async def on_new_shift_later(
        message: Message,
        config: Config,
) -> None:
    await message.answer('Хорошо! Возвращаюсь к главному меню.')
    view = MainMenuView(config.web_app_base_url)
    await answer_view(message, view)


@router.callback_query(
    F.data == CallbackDataPrefix.SHIFT_FINISH_REJECT,
    invert_f(admins_filter),
    StateFilter(ShiftFinishStates.confirm),
)
@inject
async def on_shift_finish_reject(
        callback_query: CallbackQuery,
        state: FSMContext,
) -> None:
    await state.clear()
    await callback_query.answer(
        text='❗️ Вы отменили завершение смены',
        show_alert=True,
    )
    text = format_reject_text(callback_query.message)
    await callback_query.message.edit_text(text)


@router.callback_query(
    F.data == CallbackDataPrefix.SHIFT_FINISH_ACCEPT,
    invert_f(admins_filter),
    StateFilter(ShiftFinishStates.confirm),
)
@inject
async def on_shift_finish_accept(
        callback_query: CallbackQuery,
        state: FSMContext,
        main_chat_notification_service: SpecificChatsNotificationService,
        shift_repository: ShiftRepository = Depends(
            dependency=get_shift_repository,
            use_cache=False,
        ),
) -> None:
    state_data: dict = await state.get_data()

    statement_photo_file_id: str = state_data['statement_photo_file_id']
    service_app_photo_file_id: str = state_data['service_app_photo_file_id']

    await state.clear()
    shift_finish_result = await shift_repository.finish(
        staff_id=callback_query.from_user.id,
    )

    if shift_finish_result.is_first_shift:
        view = StaffFirstShiftFinishedView()
    else:
        view = StaffShiftFinishedView()
    await callback_query.message.edit_text(
        format_accept_text(callback_query.message),
    )
    await answer_view(callback_query.message, view)

    view = StaffShiftFinishedNotificationView(
        shift_finish_result,
        photo_file_ids=(
            statement_photo_file_id,
            service_app_photo_file_id,
        ),
    )
    await main_chat_notification_service.send_media_group(view.as_media_group())


@router.callback_query(
    F.data == CallbackDataPrefix.SHIFT_FINISH_SERVICE_APP_PHOTO_CONFIRM,
    invert_f(admins_filter),
    StateFilter(ShiftFinishStates.service_app_photo),
)
async def on_service_app_photo_confirm(
        callback_query: CallbackQuery,
        state: FSMContext,
) -> None:
    await state.set_state(ShiftFinishStates.confirm)
    state_data: dict = await state.get_data()
    statement_photo_file_id: str = state_data['statement_photo_file_id']
    service_app_photo_file_id: str = state_data['service_app_photo_file_id']
    text = format_accept_text(callback_query.message)
    await callback_query.message.edit_text(text)
    view = ShiftFinishPhotosView(
        statement_photo_file_id=statement_photo_file_id,
        service_app_photo_file_id=service_app_photo_file_id,
    )
    await answer_media_group_view(
        callback_query.message,
        view,
    )
    view = ShiftFinishConfirmAllView()
    await answer_view(callback_query.message, view)


@router.message(
    F.photo,
    invert_f(admins_filter),
    StateFilter(ShiftFinishStates.service_app_photo),
)
async def on_service_app_photo_input(
        message: Message,
        state: FSMContext,
) -> None:
    file_id = message.photo[-1].file_id
    await state.update_data(service_app_photo_file_id=file_id)
    view = ShiftFinishPhotoConfirmView(
        CallbackDataPrefix.SHIFT_FINISH_SERVICE_APP_PHOTO_CONFIRM,
    )
    await answer_view(message, view)


@router.callback_query(
    F.data == CallbackDataPrefix.SHIFT_FINISH_STATEMENT_PHOTO_CONFIRM,
    invert_f(admins_filter),
    StateFilter(ShiftFinishStates.statement_photo),
)
async def on_statement_photo_confirm(
        callback_query: CallbackQuery,
        state: FSMContext,
) -> None:
    await state.set_state(ShiftFinishStates.service_app_photo)
    text = format_accept_text(callback_query.message)
    await callback_query.message.edit_text(text)
    await callback_query.message.answer(
        '🖼️ Отправьте скриншот из сервисного приложения,'
        ' на котором нет активных аренд и задач.'
        ' Не обрезайте скриншот перед отправкой.'
    )


@router.message(
    F.text,
    invert_f(admins_filter),
    StateFilter(
        ShiftFinishStates.statement_photo,
        ShiftFinishStates.service_app_photo,
    ),
)
async def on_statement_text_input(
        message: Message,
) -> None:
    await message.answer('❌ Отправьте фото')


@router.message(
    F.photo,
    invert_f(admins_filter),
    StateFilter(ShiftFinishStates.statement_photo),
)
@inject
async def on_statement_photo_input(
        message: Message,
        state: FSMContext,
        shift_repository: ShiftRepository = Depends(
            get_shift_repository,
            use_cache=False,
        ),
) -> None:
    file_id = message.photo[-1].file_id
    await shift_repository.get_active(message.from_user.id)
    await state.update_data(statement_photo_file_id=file_id)
    view = ShiftFinishPhotoConfirmView(
        CallbackDataPrefix.SHIFT_FINISH_STATEMENT_PHOTO_CONFIRM,
    )
    await answer_view(message, view)


@router.callback_query(
    F.data == CallbackDataPrefix.SHIFT_FINISH_FLOW_START_ACCEPT,
    invert_f(admins_filter),
    StateFilter('*'),
)
@inject
async def on_shift_finish_accept(
        callback_query: CallbackQuery,
        state: FSMContext,
        shift_repository: ShiftRepository = Depends(
            get_shift_repository,
            use_cache=False,
        ),
) -> None:
    await shift_repository.get_active(callback_query.from_user.id)
    await state.set_state(ShiftFinishStates.statement_photo)
    await callback_query.message.edit_text('🖼️ Отправьте ведомость')


@router.callback_query(
    F.data == CallbackDataPrefix.SHIFT_FINISH_FLOW_START_REJECT,
    invert_f(admins_filter),
    StateFilter('*'),
)
@inject
async def on_shift_finish_reject(
        callback_query: CallbackQuery,
        config: Config,
        shift_repository: ShiftRepository = Depends(
            get_shift_repository,
            use_cache=False,
        ),
) -> None:
    await shift_repository.get_active(callback_query.from_user.id)
    view = ShiftMenuView(
        staff_id=callback_query.from_user.id,
        web_app_base_url=config.web_app_base_url,
    )
    await answer_view(callback_query.message, view)
    await callback_query.answer(
        text='❗️ Вы отменили завершение смены',
        show_alert=True,
    )
    await callback_query.message.delete()


@router.message(
    F.text == ButtonText.SHIFT_END,
    invert_f(admins_filter),
    StateFilter('*'),
)
@inject
async def on_shift_finish_confirm(
        message: Message,
        shift_repository: ShiftRepository = Depends(
            get_shift_repository,
            use_cache=False,
        ),
) -> None:
    await shift_repository.get_active(message.from_user.id)
    view = ShiftFinishConfirmView()
    await answer_view(message, view)

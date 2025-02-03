from redis.asyncio import Redis
from aiogram import F, Router
from aiogram.filters import StateFilter, invert_f
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from fast_depends import Depends, inject

from callback_data.prefixes import CallbackDataPrefix
from config import Config
from dependencies.repositories import get_shift_repository
from exceptions import ShiftFinishPhotosCountExceededError
from filters import admins_filter, staff_filter
from repositories import ShiftRepository
from services.notifications import SpecificChatsNotificationService
from services.shifts import ShiftFinishPhotosState
from states import ShiftFinishStates
from ui.views import (
    answer_media_group_view, answer_photo_view,
    answer_text_view, edit_as_rejected,
)
from ui.views import ButtonText
from ui.views import MainMenuView, ShiftMenuView
from ui.views import (
    ShiftFinishConfirmAllView,
    ShiftFinishConfirmView,
    ShiftFinishPhotoConfirmView,
    ShiftFinishPhotosView,
    ShiftFinishedWithoutPhotosView, StaffFirstShiftFinishedView,
    ShiftFinishedWithPhotosView,
    StaffShiftFinishedView,
)

__all__ = ('router',)

from ui.views.base import edit_as_accepted

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
    await answer_text_view(message, view)


@router.callback_query(
    F.data == CallbackDataPrefix.SHIFT_FINISH_REJECT,
    invert_f(admins_filter),
    StateFilter(ShiftFinishStates.confirm),
)
@inject
async def on_shift_finish_reject(
        callback_query: CallbackQuery,
        state: FSMContext,
        redis: Redis,
) -> None:
    shift_finish_photos_state = ShiftFinishPhotosState(
        redis=redis,
        user_id=callback_query.from_user.id,
    )
    await shift_finish_photos_state.clear()
    await state.clear()
    await callback_query.answer(
        text='❗️ Вы отменили завершение смены',
        show_alert=True,
    )
    await edit_as_rejected(callback_query.message)


@router.callback_query(
    F.data == CallbackDataPrefix.SHIFT_FINISH_ACCEPT,
    invert_f(admins_filter),
    StateFilter(ShiftFinishStates.confirm),
)
@inject
async def on_shift_finish_accept(
        callback_query: CallbackQuery,
        state: FSMContext,
        redis: Redis,
        config: Config,
        main_chat_notification_service: SpecificChatsNotificationService,
        shift_repository: ShiftRepository = Depends(
            dependency=get_shift_repository,
            use_cache=False,
        ),
) -> None:
    shift_finish_photos_state = ShiftFinishPhotosState(
        redis=redis,
        user_id=callback_query.from_user.id,
    )
    photo_file_ids = await shift_finish_photos_state.get_photo_file_ids()

    await state.clear()

    shift_finish_result = await shift_repository.finish(
        staff_id=callback_query.from_user.id,
        photo_file_ids=photo_file_ids,
    )

    if shift_finish_result.is_first_shift:
        view = StaffFirstShiftFinishedView()
        await answer_text_view(callback_query.message, view)
    else:
        view = StaffShiftFinishedView()
        await answer_text_view(callback_query.message, view)
        view = MainMenuView(config.web_app_base_url)
        await answer_text_view(callback_query.message, view)
    await edit_as_accepted(callback_query.message)
    if shift_finish_result.finish_photo_file_ids:
        view = ShiftFinishedWithPhotosView(shift_finish_result)
        await main_chat_notification_service.send_media_group(
            view.as_media_group(),
        )
    else:
        view = ShiftFinishedWithoutPhotosView(shift_finish_result)
        await main_chat_notification_service.send_view(view)


@router.callback_query(
    F.data == CallbackDataPrefix.SHIFT_FINISH_PHOTO_DELETE,
    staff_filter,
    StateFilter(
        ShiftFinishStates.statement_photo,
        ShiftFinishStates.service_app_photo,
    ),
)
async def on_shift_finish_photo_delete(
        callback_query: CallbackQuery,
        redis: Redis,
) -> None:
    file_id = callback_query.message.photo[-1].file_id
    shift_finish_photos_state = ShiftFinishPhotosState(
        redis=redis,
        user_id=callback_query.from_user.id,
    )
    await shift_finish_photos_state.delete_photo_file_id(file_id)
    await callback_query.message.delete()
    await callback_query.answer('❌ Фотография удалена', show_alert=True)


@router.callback_query(
    F.data == CallbackDataPrefix.SHIFT_FINISH_PHOTO_NEXT_STEP,
    staff_filter,
    StateFilter(
        ShiftFinishStates.statement_photo,
        ShiftFinishStates.service_app_photo,
    ),
)
async def on_next_step(
        callback_query: CallbackQuery,
        redis: Redis,
        state: FSMContext,
) -> None:
    state_string = await state.get_state()
    await callback_query.message.delete_reply_markup()
    if state_string == ShiftFinishStates.statement_photo.state:
        await state.set_state(ShiftFinishStates.service_app_photo)
        await callback_query.message.answer(
            '🖼️ Отправьте скриншот из сервисного приложения,'
            ' на котором нет активных аренд и задач.'
            ' Не обрезайте скриншот перед отправкой.'
        )
        return

    await state.set_state(ShiftFinishStates.confirm)
    shift_finish_photos_state = ShiftFinishPhotosState(
        redis=redis,
        user_id=callback_query.from_user.id,
    )
    photo_file_ids = await shift_finish_photos_state.get_photo_file_ids()

    view = ShiftFinishPhotosView(photo_file_ids)
    await answer_media_group_view(
        callback_query.message,
        view,
    )
    view = ShiftFinishConfirmAllView()
    await answer_text_view(callback_query.message, view)


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
    StateFilter(
        ShiftFinishStates.statement_photo,
        ShiftFinishStates.service_app_photo,
    ),
)
@inject
async def on_photo_input(
        message: Message,
        redis: Redis,
        shift_repository: ShiftRepository = Depends(
            get_shift_repository,
            use_cache=False,
        ),
) -> None:
    file_id = message.photo[-1].file_id
    shift_finish_photos_state = ShiftFinishPhotosState(
        redis=redis,
        user_id=message.from_user.id,
    )
    try:
        await shift_finish_photos_state.add_photo_file_id(file_id)
    except ShiftFinishPhotosCountExceededError:
        await message.answer('❌ Вы не можете загрузить больше 10 фотографий')
    else:
        await shift_repository.get_active(message.from_user.id)
        view = ShiftFinishPhotoConfirmView(file_id)
        await answer_photo_view(message, view)


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
    await answer_text_view(callback_query.message, view)
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
        redis: Redis,
        shift_repository: ShiftRepository = Depends(
            get_shift_repository,
            use_cache=False,
        ),
) -> None:
    shift_finish_photos_state = ShiftFinishPhotosState(
        redis=redis,
        user_id=message.from_user.id,
    )
    await shift_finish_photos_state.clear()
    await shift_repository.get_active(message.from_user.id)
    view = ShiftFinishConfirmView()
    await answer_text_view(message, view)

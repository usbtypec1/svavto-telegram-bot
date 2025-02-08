from aiogram import Bot, F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from fast_depends import Depends, inject

from callback_data.prefixes import CallbackDataPrefix
from config import Config
from dependencies.repositories import (
    get_economics_repository,
)
from filters import admins_filter
from repositories import EconomicsRepository
from states import PenaltyCreateStates
from ui.views import (
    AdminMenuView, answer_text_view, edit_as_rejected, edit_message_by_view,
    PenaltyCreateNotificationView, PenaltyCreateSuccessView,
    PhotoCreateWithPhotoNotificationView, send_photo_view, send_text_view,
)

__all__ = ('router',)

router = Router(name=__name__)


@router.callback_query(
    F.data == CallbackDataPrefix.PENALTY_CREATE_REJECT,
    admins_filter,
    StateFilter(PenaltyCreateStates.confirm),
)
async def on_reject_penalty_creation(
        callback_query: CallbackQuery,
        state: FSMContext,
        config: Config,
) -> None:
    await state.clear()
    await edit_as_rejected(callback_query.message)
    view = AdminMenuView(config.web_app_base_url)
    await answer_text_view(callback_query.message, view)


@router.callback_query(
    F.data == CallbackDataPrefix.PENALTY_CREATE_ACCEPT,
    admins_filter,
    StateFilter(PenaltyCreateStates.confirm),
)
@inject
async def on_accept_penalty_creation(
        callback_query: CallbackQuery,
        state: FSMContext,
        bot: Bot,
        config: Config,
        economics_repository: EconomicsRepository = Depends(
            dependency=get_economics_repository,
            use_cache=False,
        ),
) -> None:
    state_data = await state.get_data()
    shift_id: int = state_data['shift_id']
    reason: str = state_data['reason']
    amount: int | None = state_data.get('amount')
    photo_file_id: str | None = state_data.get('photo_file_id')

    penalty = await economics_repository.create_penalty(
        shift_id=shift_id,
        reason=reason,
        amount=amount,
    )

    view = PenaltyCreateSuccessView(penalty)
    await edit_message_by_view(callback_query.message, view)

    view = AdminMenuView(config.web_app_base_url)
    await answer_text_view(callback_query.message, view)

    if photo_file_id is None:
        view = PenaltyCreateNotificationView(
            penalty=penalty,
            web_app_base_url=config.web_app_base_url,
        )
        await send_text_view(bot, view, penalty.staff_id)
    else:
        view = PhotoCreateWithPhotoNotificationView(
            penalty=penalty,
            web_app_base_url=config.web_app_base_url,
            photo_file_id=photo_file_id,
        )
        await send_photo_view(bot, view, penalty.staff_id)

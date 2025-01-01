from aiogram import Bot, F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from fast_depends import Depends, inject

from callback_data.prefixes import CallbackDataPrefix
from config import Config
from dependencies.repositories import (
    get_economics_repository,
    get_staff_repository,
)
from filters import admins_filter
from repositories import EconomicsRepository, StaffRepository
from services.telegram_events import format_reject_text
from states import PenaltyCreateStates
from views.admins import AdminMenuView
from views.base import (
    answer_view, edit_message_by_view, send_photo_view,
    send_view,
)
from views.penalties import (
    PenaltyCreateNotificationView,
    PenaltyCreateSuccessView, PhotoCreateWithPhotoNotificationView,
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
    await callback_query.message.edit_text(
        format_reject_text(callback_query.message),
    )
    view = AdminMenuView(config.web_app_base_url)
    await answer_view(callback_query.message, view)


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
        staff_repository: StaffRepository = Depends(
            dependency=get_staff_repository,
            use_cache=False,
        ),
) -> None:
    state_data = await state.get_data()
    staff_id: int = state_data['staff_id']
    shift_id: int = state_data['shift_id']
    reason: str = state_data['reason']
    amount: int | None = state_data.get('amount')
    photo_file_id: str | None = state_data.get('photo_file_id')

    penalty = await economics_repository.create_penalty(
        staff_id=staff_id,
        shift_id=shift_id,
        reason=reason,
        amount=amount,
    )
    staff = await staff_repository.get_by_id(staff_id)

    view = PenaltyCreateSuccessView(penalty, staff)
    await edit_message_by_view(callback_query.message, view)

    view = AdminMenuView(config.web_app_base_url)
    await answer_view(callback_query.message, view)

    if photo_file_id is None:
        view = PenaltyCreateNotificationView(
            penalty=penalty,
            web_app_base_url=config.web_app_base_url,
        )
        await send_view(bot, view, staff.id)
    else:
        view = PhotoCreateWithPhotoNotificationView(
            penalty=penalty,
            web_app_base_url=config.web_app_base_url,
            photo_file_id=photo_file_id,
        )
        await send_photo_view(bot, view, staff.id)

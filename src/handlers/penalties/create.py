from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from fast_depends import Depends, inject

from callback_data import PenaltyCreateChooseStaffCallbackData, \
    PenaltyCreateChooseReasonCallbackData
from callback_data.prefixes import CallbackDataPrefix
from config import Config
from dependencies.repositories import get_staff_repository, \
    get_economics_repository
from enums import PenaltyReason
from filters import admins_filter
from repositories import StaffRepository, EconomicsRepository
from services.telegram_events import format_reject_text
from states import PenaltyCreateStates
from views.admins import AdminMenuView
from views.base import answer_view, edit_message_by_view
from views.button_texts import ButtonText
from views.penalties import (
    PenaltyCreateChooseStaffView,
    PenaltyCreateInputOtherReasonView,
    PenaltyCreateChooseReasonView, PenaltyCreateConfirmView,
    PenaltyCreateSuccessView,
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
    reason: str = state_data['reason']
    penalty = await economics_repository.create_penalty(
        staff_id=staff_id,
        reason=reason,
    )
    staff = await staff_repository.get_by_id(staff_id)
    view = PenaltyCreateSuccessView(penalty, staff)
    await edit_message_by_view(callback_query.message, view)
    view = AdminMenuView(config.web_app_base_url)
    await answer_view(callback_query.message, view)


@router.message(
    F.text,
    admins_filter,
    StateFilter(PenaltyCreateStates.reason),
)
@inject
async def on_input_other_reason_for_penalty(
        message: Message,
        state: FSMContext,
        staff_repository: StaffRepository = Depends(
            dependency=get_staff_repository,
            use_cache=False,
        ),
) -> None:
    reason = message.text
    await state.update_data(reason=reason)
    await state.set_state(PenaltyCreateStates.confirm)
    state_data = await state.get_data()
    staff_id: int = state_data['staff_id']
    staff = await staff_repository.get_by_id(staff_id)
    view = PenaltyCreateConfirmView(staff=staff, reason=reason)
    await answer_view(message, view)


@router.callback_query(
    PenaltyCreateChooseReasonCallbackData.filter(),
    admins_filter,
    StateFilter(PenaltyCreateStates.reason),
)
@inject
async def on_choose_reason_for_penalty(
        callback_query: CallbackQuery,
        state: FSMContext,
        callback_data: PenaltyCreateChooseReasonCallbackData,
        staff_repository: StaffRepository = Depends(
            dependency=get_staff_repository,
            use_cache=False,
        ),
) -> None:
    reason_to_text: dict[PenaltyReason: str] = {
        PenaltyReason.NOT_SHOWING_UP: 'Невыход',
        PenaltyReason.EARLY_LEAVE: 'Ранний уход',
        PenaltyReason.LATE_REPORT: 'Отчет не вовремя',
    }
    reason: str = reason_to_text.get(callback_data.reason, callback_data.reason)
    await state.update_data(reason=reason)
    await state.set_state(PenaltyCreateStates.confirm)
    state_data = await state.get_data()
    staff_id: int = state_data['staff_id']
    staff = await staff_repository.get_by_id(staff_id)
    view = PenaltyCreateConfirmView(staff=staff, reason=reason)
    await answer_view(callback_query.message, view)


@router.callback_query(
    PenaltyCreateChooseStaffCallbackData.filter(),
    admins_filter,
    StateFilter(PenaltyCreateStates.staff),
)
async def on_choose_staff_for_penalty(
        callback_query: CallbackQuery,
        state: FSMContext,
        callback_data: PenaltyCreateChooseStaffCallbackData,
) -> None:
    await state.update_data(staff_id=callback_data.staff_id)
    await state.set_state(PenaltyCreateStates.reason)
    view = PenaltyCreateChooseReasonView()
    await edit_message_by_view(callback_query.message, view)
    view = PenaltyCreateInputOtherReasonView()
    await answer_view(callback_query.message, view)


@router.message(
    F.text == ButtonText.PENALTY,
    admins_filter,
    StateFilter('*'),
)
@inject
async def on_start_penalty_create_flow(
        message: Message,
        state: FSMContext,
        staff_repository: StaffRepository = Depends(
            dependency=get_staff_repository,
            use_cache=False,
        ),
) -> None:
    staff_list = await staff_repository.get_all()
    view = PenaltyCreateChooseStaffView(staff_list)
    await state.set_state(PenaltyCreateStates.staff)
    await answer_view(message, view)

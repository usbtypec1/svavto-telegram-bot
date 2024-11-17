from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from fast_depends import Depends, inject

from callback_data import PenaltyCreateChooseReasonCallbackData
from dependencies.repositories import get_staff_repository
from enums import PenaltyReason
from filters import admins_filter
from repositories import StaffRepository
from states import PenaltyCreateStates
from views.base import edit_message_by_view
from views.penalties import PenaltyCreateConfirmView, penalty_reason_to_name

__all__ = ('router',)

router = Router(name=__name__)


@router.message(
    F.text,
    admins_filter,
    StateFilter(PenaltyCreateStates.reason),
)
async def on_input_other_reason_for_penalty(
        message: Message,
        state: FSMContext,
) -> None:
    await state.update_data(reason=message.text)
    await state.set_state(PenaltyCreateStates.amount)
    await message.answer('💰 Введите сумму штрафа')


@router.callback_query(
    PenaltyCreateChooseReasonCallbackData.filter(
        F.reason == PenaltyReason.OTHER,
    ),
    admins_filter,
    StateFilter(PenaltyCreateStates.reason),
)
async def on_choose_reason_for_penalty(
        callback_query: CallbackQuery,
) -> None:
    await callback_query.message.edit_text('✏️ Введите причину штрафа')
    await callback_query.answer()


@router.callback_query(
    PenaltyCreateChooseReasonCallbackData.filter(
        F.reason != PenaltyReason.OTHER,
    ),
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
    reason_name: str = penalty_reason_to_name.get(
        callback_data.reason,
        callback_data.reason,
    )
    state_data = await state.update_data(reason=callback_data.reason)
    staff_id: int = state_data['staff_id']
    staff = await staff_repository.get_by_id(staff_id)
    await state.set_state(PenaltyCreateStates.confirm)
    view = PenaltyCreateConfirmView(
        staff=staff,
        reason=reason_name,
        amount=None,
    )
    await edit_message_by_view(callback_query.message, view)

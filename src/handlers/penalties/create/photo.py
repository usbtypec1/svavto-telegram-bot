from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from fast_depends import Depends, inject

from callback_data.prefixes import CallbackDataPrefix
from dependencies.repositories import get_staff_repository
from filters import admins_filter
from repositories import StaffRepository
from states import PenaltyCreateStates
from views.base import answer_view
from views.penalties import PenaltyCreateConfirmView

__all__ = ('router',)

router = Router(name=__name__)


@router.callback_query(
    F.data == CallbackDataPrefix.SKIP,
    admins_filter,
    StateFilter(PenaltyCreateStates.photo),
)
@inject
async def on_skip_penalty_photo(
        callback_query: CallbackQuery,
        state: FSMContext,
        staff_repository: StaffRepository = Depends(
            dependency=get_staff_repository,
            use_cache=False,
        ),
) -> None:
    state_data: dict = await state.get_data()
    reason: str = state_data['reason']
    amount: int = state_data['amount']
    staff_id: int = state_data['staff_id']

    staff = await staff_repository.get_by_id(staff_id)

    await state.set_state(PenaltyCreateStates.confirm)

    view = PenaltyCreateConfirmView(
        staff=staff,
        reason=reason,
        amount=amount,
    )
    await callback_query.message.edit_text('📸 Фото штрафа пропущено')
    await answer_view(callback_query.message, view)


@router.message(
    F.photo,
    admins_filter,
    StateFilter(PenaltyCreateStates.photo),
)
@inject
async def on_input_penalty_photo(
        message: Message,
        state: FSMContext,
        staff_repository: StaffRepository = Depends(
            dependency=get_staff_repository,
            use_cache=False,
        ),
) -> None:
    state_data: dict = await state.get_data()
    reason: str = state_data['reason']
    amount: int = state_data['amount']
    staff_id: int = state_data['staff_id']

    staff = await staff_repository.get_by_id(staff_id)

    await state.set_state(PenaltyCreateStates.confirm)

    view = PenaltyCreateConfirmView(
        staff=staff,
        reason=reason,
        amount=amount,
    )
    await answer_view(message, view)

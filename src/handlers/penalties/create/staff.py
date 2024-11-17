from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from fast_depends import Depends, inject

from callback_data import PenaltyCreateChooseStaffCallbackData
from dependencies.repositories import get_staff_repository
from enums import StaffOrderBy
from filters import admins_filter
from repositories import StaffRepository
from states import PenaltyCreateStates
from views.base import answer_view, edit_message_by_view
from views.button_texts import ButtonText
from views.penalties import (
    PenaltyCreateChooseReasonView,
    PenaltyCreateChooseStaffView,
)

__all__ = ('router',)

router = Router(name=__name__)


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
    staff_list = await staff_repository.get_all(
        order_by=StaffOrderBy.FULL_NAME_ASC,
    )
    view = PenaltyCreateChooseStaffView(staff_list)
    await state.set_state(PenaltyCreateStates.staff)
    await answer_view(message, view)

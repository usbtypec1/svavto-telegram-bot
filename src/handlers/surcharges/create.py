from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from fast_depends import Depends, inject

from callback_data import SurchargeCreateChooseStaffCallbackData
from callback_data.prefixes import CallbackDataPrefix
from dependencies.repositories import (
    get_staff_repository,
    get_economics_repository,
)
from exceptions.surcharges import SurchargeAmountParseError
from filters import admins_filter
from repositories import StaffRepository, EconomicsRepository
from services.surcharges import parse_money_amount
from states import SurchargeCreateStates
from views.base import answer_view, edit_message_by_view
from views.button_texts import ButtonText
from views.surcharges import (
    SurchargeCreateChooseStaffView,
    SurchargeCreateInputReasonView,
    SurchargeCreateConfirmView,
    SurchargeCreateSuccessView,
    SurchargeCreateInputAmountView,
)

__all__ = ('router',)

router = Router(name=__name__)


@router.callback_query(
    F.data == CallbackDataPrefix.SURCHARGE_CREATE_REJECT,
    admins_filter,
    StateFilter(SurchargeCreateStates.confirm),
)
async def on_reject_surcharge_creation(
        callback_query: CallbackQuery,
        state: FSMContext,
) -> None:
    await state.clear()
    await callback_query.message.edit_text(
        f'{callback_query.message.text}\n\n<i>Отменено</i>',
    )


@router.callback_query(
    F.data == CallbackDataPrefix.SURCHARGE_CREATE_ACCEPT,
    admins_filter,
    StateFilter(SurchargeCreateStates.confirm),
)
@inject
async def on_accept_surcharge_creation(
        callback_query: CallbackQuery,
        state: FSMContext,
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
    amount: int = state_data['amount']
    surcharge = await economics_repository.create_surcharge(
        staff_id=staff_id,
        reason=reason,
        amount=amount,
    )
    staff = await staff_repository.get_by_id(staff_id)
    view = SurchargeCreateSuccessView(surcharge, staff)
    await edit_message_by_view(callback_query.message, view)


@router.message(
    F.text,
    admins_filter,
    StateFilter(SurchargeCreateStates.amount),
)
@inject
async def on_input_amount_for_surcharge(
        message: Message,
        state: FSMContext,
        staff_repository: StaffRepository = Depends(
            dependency=get_staff_repository,
            use_cache=False,
        ),
) -> None:
    try:
        amount = parse_money_amount(message.text)
    except SurchargeAmountParseError:
        await message.reply('Неверный формат суммы. Попробуйте ещё раз.')
        return

    await state.update_data(amount=amount)
    await state.set_state(SurchargeCreateStates.confirm)
    state_data = await state.get_data()
    staff_id: int = state_data['staff_id']
    reason: str = state_data['reason']
    staff = await staff_repository.get_by_id(staff_id)
    view = SurchargeCreateConfirmView(staff=staff, reason=reason, amount=amount)
    await answer_view(message, view)


@router.message(
    F.text,
    admins_filter,
    StateFilter(SurchargeCreateStates.reason),
)
async def on_input_reason_for_surcharge(
        message: Message,
        state: FSMContext,
) -> None:
    reason = message.text
    await state.update_data(reason=reason)
    await state.set_state(SurchargeCreateStates.amount)
    view = SurchargeCreateInputAmountView()
    await answer_view(message, view)


@router.callback_query(
    SurchargeCreateChooseStaffCallbackData.filter(),
    admins_filter,
    StateFilter(SurchargeCreateStates.staff),
)
async def on_choose_staff_for_surcharge(
        callback_query: CallbackQuery,
        state: FSMContext,
        callback_data: SurchargeCreateChooseStaffCallbackData,
) -> None:
    await state.update_data(staff_id=callback_data.staff_id)
    await state.set_state(SurchargeCreateStates.reason)
    view = SurchargeCreateInputReasonView()
    await answer_view(callback_query.message, view)


@router.message(
    F.text == ButtonText.SURCHARGE,
    admins_filter,
    StateFilter('*'),
)
@inject
async def on_start_surcharge_create_flow(
        message: Message,
        state: FSMContext,
        staff_repository: StaffRepository = Depends(
            dependency=get_staff_repository,
            use_cache=False,
        ),
) -> None:
    staff_list = await staff_repository.get_all()
    view = SurchargeCreateChooseStaffView(staff_list)
    await state.set_state(SurchargeCreateStates.staff)
    await answer_view(message, view)

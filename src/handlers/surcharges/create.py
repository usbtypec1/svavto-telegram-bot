from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from fast_depends import Depends, inject

from callback_data import SurchargeCreateChooseStaffCallbackData
from callback_data.prefixes import CallbackDataPrefix
from config import Config
from dependencies.repositories import (
    get_economics_repository,
    get_staff_repository,
)
from enums import StaffOrderBy
from exceptions.surcharges import SurchargeAmountParseError
from filters import admins_filter
from models import SpecificShiftPickResult
from repositories import EconomicsRepository, StaffRepository
from services.surcharges import parse_money_amount
from states import SurchargeCreateStates
from ui.views import AdminMenuView, edit_as_rejected
from ui.views import answer_text_view, edit_message_by_view
from ui.views import ButtonText
from ui.views import SpecificShiftPickerView
from ui.views import (
    SurchargeCreateChooseStaffView,
    SurchargeCreateConfirmView,
    SurchargeCreateInputAmountView,
    SurchargeCreateInputReasonView,
    SurchargeCreateSuccessView,
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
        config: Config,
        state: FSMContext,
) -> None:
    await state.clear()
    await edit_as_rejected(callback_query.message)
    view = AdminMenuView(config.web_app_base_url)
    await answer_text_view(callback_query.message, view)


@router.callback_query(
    F.data == CallbackDataPrefix.SURCHARGE_CREATE_ACCEPT,
    admins_filter,
    StateFilter(SurchargeCreateStates.confirm),
)
@inject
async def on_accept_surcharge_creation(
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
    shift_id: int = state_data['shift_id']
    reason: str = state_data['reason']
    amount: int = state_data['amount']

    surcharge = await economics_repository.create_surcharge(
        staff_id=staff_id,
        shift_id=shift_id,
        reason=reason,
        amount=amount,
    )
    staff = await staff_repository.get_by_id(staff_id)

    view = SurchargeCreateSuccessView(surcharge, staff)
    await edit_message_by_view(callback_query.message, view)
    view = AdminMenuView(config.web_app_base_url)
    await answer_text_view(callback_query.message, view)


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
    await answer_text_view(message, view)


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
    await answer_text_view(message, view)


@router.message(
    F.web_app_data.button_text == ButtonText.SPECIFIC_SHIFT,
    admins_filter,
    StateFilter(SurchargeCreateStates.shift),
)
async def on_pick_specific_shift(
        message: Message,
        state: FSMContext,
) -> None:
    specific_shift_pick_result = SpecificShiftPickResult.model_validate_json(
        json_data=message.web_app_data.data,
    )
    await state.update_data(shift_id=specific_shift_pick_result.shift_id)
    await state.set_state(SurchargeCreateStates.reason)
    view = SurchargeCreateInputReasonView()
    await message.answer(
        text='✅ Смена выбрана',
        reply_markup=ReplyKeyboardRemove(),
    )
    await answer_text_view(message, view)


@router.callback_query(
    SurchargeCreateChooseStaffCallbackData.filter(),
    admins_filter,
    StateFilter(SurchargeCreateStates.staff),
)
async def on_choose_staff_for_surcharge(
        callback_query: CallbackQuery,
        state: FSMContext,
        callback_data: SurchargeCreateChooseStaffCallbackData,
        config: Config,
) -> None:
    await state.update_data(staff_id=callback_data.staff_id)
    await state.set_state(SurchargeCreateStates.shift)
    view = SpecificShiftPickerView(
        web_app_base_url=config.web_app_base_url,
        staff_id=callback_data.staff_id,
    )
    await answer_text_view(callback_query.message, view)


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
    staff_list = await staff_repository.get_all(
        order_by=StaffOrderBy.FULL_NAME_ASC,
    )
    view = SurchargeCreateChooseStaffView(staff_list.staff)
    await state.set_state(SurchargeCreateStates.staff)
    await answer_text_view(message, view)

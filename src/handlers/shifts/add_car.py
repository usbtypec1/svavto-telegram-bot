from aiogram import Router, F
from aiogram.filters import StateFilter, invert_f
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from callback_data import CarClassChoiceCallbackData, \
    WashTypeChoiceCallbackData, WindshieldWasherRefilledValueCallbackData
from callback_data.prefixes import CallbackDataPrefix
from filters import admins_filter
from states import ShiftAddCarStates
from views.base import answer_or_edit_message_by_view, edit_message_by_view
from views.button_texts import ButtonText
from views.shifts import (
    CarNumberInputView,
    CarClassInputView,
    WashTypeInputView,
    WindshieldWasherRefilledInputView,
    WindshieldWasherRefilledValueInputView,
    AdditionalServicesIncludedInputView,
    AddCarWithoutAdditionalServicesConfirmView,
)

__all__ = ('router',)

router = Router(name=__name__)


@router.callback_query(
    F.data == CallbackDataPrefix.ADD_CAR_CONFIRM,
    invert_f(admins_filter),
    StateFilter(ShiftAddCarStates.additional_services),
)
async def on_add_car_flow_confirm_without_additional_services(
        callback_query: CallbackQuery,
        state: FSMContext,
) -> None:
    data = await state.get_data()
    await state.clear()
    view = AddCarWithoutAdditionalServicesConfirmView(data['car_number'])
    await edit_message_by_view(callback_query.message, view)


@router.callback_query(
    WindshieldWasherRefilledValueCallbackData.filter(),
    invert_f(admins_filter),
    StateFilter(
        ShiftAddCarStates.windshield_washer_refilled_value,
        ShiftAddCarStates.is_windshield_washer_refilled,
    )
)
async def on_has_additional_services(
        callback_query: CallbackQuery,
        callback_data: WindshieldWasherRefilledValueCallbackData,
        state: FSMContext,
) -> None:
    await state.set_state(ShiftAddCarStates.additional_services)
    await state.update_data(
        windshield_washer_refilled_value=callback_data.value,
    )
    view = AdditionalServicesIncludedInputView()
    await edit_message_by_view(callback_query.message, view)


@router.callback_query(
    F.data == CallbackDataPrefix.WINDSHIELD_WASHER_REFILLED_VALUE,
    invert_f(admins_filter),
    StateFilter(ShiftAddCarStates.is_windshield_washer_refilled),
)
async def on_windshield_washer_refilled(
        callback_query: CallbackQuery,
        state: FSMContext,
) -> None:
    await state.update_data(is_windshield_washer_refilled=True)
    await state.set_state(ShiftAddCarStates.windshield_washer_refilled_value)
    view = WindshieldWasherRefilledValueInputView()
    await edit_message_by_view(callback_query.message, view)


@router.callback_query(
    WashTypeChoiceCallbackData.filter(),
    invert_f(admins_filter),
    StateFilter(ShiftAddCarStates.wash_type)
)
async def on_wash_type_chosen(
        callback_query: CallbackQuery,
        callback_data: WashTypeChoiceCallbackData,
        state: FSMContext,
) -> None:
    await state.update_data(wash_type=callback_data.wash_type)
    await state.set_state(ShiftAddCarStates.is_windshield_washer_refilled)
    view = WindshieldWasherRefilledInputView()
    await edit_message_by_view(callback_query.message, view)


@router.callback_query(
    CarClassChoiceCallbackData.filter(),
    invert_f(admins_filter),
    StateFilter(ShiftAddCarStates.car_class)
)
async def on_car_class_chosen(
        callback_query: CallbackQuery,
        callback_data: CarClassChoiceCallbackData,
        state: FSMContext,
) -> None:
    await state.update_data(car_class=callback_data.car_class)
    await state.set_state(ShiftAddCarStates.wash_type)
    view = WashTypeInputView()
    await edit_message_by_view(callback_query.message, view)


@router.message(
    F.text,
    invert_f(admins_filter),
    StateFilter(ShiftAddCarStates.car_number)
)
async def on_car_number_entered(
        message_or_callback_query: Message | CallbackQuery,
        state: FSMContext,
) -> None:
    if isinstance(message_or_callback_query, Message):
        car_number = message_or_callback_query.text
        await state.update_data(car_number=car_number)
    else:
        await on_start_shift_add_car_flow(message_or_callback_query, state)
    await state.set_state(ShiftAddCarStates.car_class)
    view = CarClassInputView()
    await answer_or_edit_message_by_view(message_or_callback_query, view)


@router.message(
    F.text == ButtonText.SHIFT_ADD_CAR,
    invert_f(admins_filter),
    StateFilter('*'),
)
@router.callback_query(
    F.data == CallbackDataPrefix.CAR_NUMBER,
    invert_f(admins_filter),
    StateFilter('*'),
)
async def on_start_shift_add_car_flow(
        message_or_callback_query: Message | CallbackQuery,
        state: FSMContext,
) -> None:
    await state.set_state(ShiftAddCarStates.car_number)
    view = CarNumberInputView()
    await answer_or_edit_message_by_view(message_or_callback_query, view)

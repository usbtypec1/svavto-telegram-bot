from multiprocessing.managers import State

from aiogram import Router, F

from aiogram.filters import StateFilter, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ForceReply

from states import StaffRegisterStates

from views.base import answer_view

from views.register import StaffRegisterConfirmView

__all__ = ('router',)

router = Router(name=__name__)


@router.callback_query(
    F.data == 'register-confirm',
    StateFilter(StaffRegisterStates.console_phone_number),
)
async def on_performer_register_confirm(
        callback_query: CallbackQuery,
        state: FSMContext,
) -> None:
    state_data = await state.get_data()
    print(state_data)


@router.message(
    F.text,
    StateFilter(StaffRegisterStates.console_phone_number),
)
async def on_console_phone_number_input(
        message: Message,
        state: FSMContext,
) -> None:
    state_data = await state.get_data()
    await state.update_data(console_phone_number=message.text)
    view = StaffRegisterConfirmView(
        full_name=state_data['full_name'],
        car_sharing_phone_number=state_data['car_sharing_phone_number_input'],
        console_phone_number=message.text,
    )
    await answer_view(message, view)


@router.message(
    F.text,
    StateFilter(StaffRegisterStates.car_sharing_phone_number),
)
async def on_car_sharing_phone_number_input(
        message: Message,
        state: FSMContext,
) -> None:
    await state.update_data(car_sharing_phone_number_input=message.text)
    await state.set_state(StaffRegisterStates.console_phone_number)
    await message.answer(
        'Введите номер телефона, указанный в компании Консоль:',
        reply_markup=ForceReply(input_field_placeholder='Номер телефона'),
    )


@router.message(
    F.text,
    StateFilter(StaffRegisterStates.full_name),
)
async def on_full_name_input(message: Message, state: FSMContext) -> None:
    await state.update_data(full_name=message.text)
    await state.set_state(StaffRegisterStates.car_sharing_phone_number)
    await message.answer(
        'Введите номер телефона, привязанный к аккаунту в каршеринге:',
        reply_markup=ForceReply(input_field_placeholder='Номер телефона'),
    )


@router.callback_query(
    F.data == 'register',
    StateFilter('*'),
)
async def on_start_registration(
        callback_query: CallbackQuery,
        state: FSMContext,
) -> None:
    await state.set_state(StaffRegisterStates.full_name)
    await callback_query.message.answer(
        'Введите ваше ФИО:',
        reply_markup=ForceReply(input_field_placeholder='ФИО'),
    )

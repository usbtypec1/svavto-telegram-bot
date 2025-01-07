from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from fast_depends import Depends, inject

from callback_data.prefixes import CallbackDataPrefix
from dependencies.repositories import get_car_wash_repository
from filters import admins_filter
from repositories import CarWashRepository
from states import CarWashCreateStates
from views.base import edit_message_by_view, answer_text_view
from views.car_washes import CarWashCreateNameInputView, CarWashCreateConfirmView, \
    CarWashListView

__all__ = ('router',)

router = Router(name='create-car-wash')


@router.callback_query(
    F.data == CallbackDataPrefix.CAR_WASH_CREATE_CONFIRM,
    admins_filter,
    StateFilter(CarWashCreateStates.confirm),
)
@inject
async def on_car_wash_create_confirmed(
        callback_query: CallbackQuery,
        state: FSMContext,
        car_wash_repository: CarWashRepository = Depends(
            dependency=get_car_wash_repository,
            use_cache=False,
        ),
) -> None:
    state_data: dict = await state.get_data()
    await state.clear()
    car_wash_name: str = state_data['car_wash_name']
    await car_wash_repository.create(car_wash_name)
    await callback_query.message.edit_text('✅ Мойка добавлена')
    car_washes = await car_wash_repository.get_all()
    view = CarWashListView(car_washes)
    await answer_text_view(callback_query.message, view)


@router.message(
    admins_filter,
    StateFilter(CarWashCreateStates.name),
)
async def on_car_wash_name_entered(
        message: Message,
        state: FSMContext,
) -> None:
    car_wash_name = message.text
    await state.set_state(CarWashCreateStates.confirm)
    await state.update_data(car_wash_name=car_wash_name)
    view = CarWashCreateConfirmView(car_wash_name)
    await answer_text_view(message, view)


@router.callback_query(
    F.data == CallbackDataPrefix.CAR_WASH_CREATE,
    admins_filter,
    StateFilter('*'),
)
async def on_start_car_wash_create_flow(
        callback_query: CallbackQuery,
        state: FSMContext,
):
    await state.set_state(CarWashCreateStates.name)
    view = CarWashCreateNameInputView()
    await edit_message_by_view(callback_query.message, view)

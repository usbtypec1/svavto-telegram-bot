from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from fast_depends import inject

from callback_data.prefixes import CallbackDataPrefix
from dependencies.repositories import (
    ShiftRepositoryDependency,
)
from filters import staff_filter
from states import DryCleaningRequestStates
from ui.views import answer_view, ButtonText, DryCleaningCarNumberView


router = Router(name=__name__)


@router.message(
    F.text == ButtonText.SHIFT_DRY_CLEANING_REQUEST,
    staff_filter,
    StateFilter('*'),
)
@inject
async def on_dry_cleaning_request_start_flow(
        message: Message,
        state: FSMContext,
        shift_repository: ShiftRepositoryDependency,
) -> None:
    shift_id = await shift_repository.get_active(message.from_user.id)
    transferred_cars_response = await shift_repository.get_transferred_cars(
        shift_id=shift_id,
    )
    await state.set_state(DryCleaningRequestStates.car)
    car_numbers = [
        car.number for car in transferred_cars_response.transferred_cars
    ]
    view = DryCleaningCarNumberView(car_numbers)
    await answer_view(message, view)


@router.callback_query(
    F.data == CallbackDataPrefix.CAR_NUMBER_INPUT,
    staff_filter,
    StateFilter(DryCleaningRequestStates.car),
)
async def on_car_number_manual_input(callback_query: CallbackQuery) -> None:
    await callback_query.message.answer(
        text='Введите номер автомобиля',
    )


@router.message(
    staff_filter,
    StateFilter(DryCleaningRequestStates.car),
)
async def on_car_number_input(
        message: Message,
        state: FSMContext,
) -> None:
    await state.update_data(car_number=message.text)


@router.callback_query(
    staff_filter,
    StateFilter(DryCleaningRequestStates.car),
)
async def on_choose_car(
        callback_query: CallbackQuery,
        state: FSMContext,
):
    await state.update_data(car_number=callback_query.data)
    await callback_query.message.answer(
        text='Загрузите фотографии загрязненных элементов',
    )


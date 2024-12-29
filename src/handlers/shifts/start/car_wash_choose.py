import datetime

from aiogram import Router
from aiogram.filters import StateFilter, invert_f
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from fast_depends import Depends, inject

from callback_data import ShiftStartCallbackData, ShiftStartCarWashCallbackData
from config import Config
from dependencies.repositories import (
    get_car_wash_repository,
    get_shift_repository,
)
from filters import admins_filter
from repositories import CarWashRepository, ShiftRepository
from states import ShiftStartStates
from views.base import answer_view, edit_message_by_view
from views.menu import ShiftMenuView
from views.shifts import ShiftStartCarWashChooseView

__all__ = ('router',)

router = Router(name=__name__)


@router.callback_query(
    ShiftStartCallbackData.filter(),
    invert_f(admins_filter),
    StateFilter('*'),
)
@inject
async def on_start_shift(
        callback_query: CallbackQuery,
        callback_data: ShiftStartCallbackData,
        state: FSMContext,
        car_wash_repository: CarWashRepository = Depends(
            dependency=get_car_wash_repository,
            use_cache=False,
        ),
) -> None:
    car_washes = await car_wash_repository.get_all()
    if not car_washes:
        await callback_query.answer(
            text='❌ Нет доступных моек',
            show_alert=True,
        )
        return
    await state.update_data(shift_id=callback_data.shift_id)
    await state.set_state(ShiftStartStates.car_wash)
    view = ShiftStartCarWashChooseView(car_washes)
    await edit_message_by_view(callback_query.message, view)


@router.callback_query(
    ShiftStartCarWashCallbackData.filter(),
    invert_f(admins_filter),
    StateFilter(ShiftStartStates.car_wash),
)
@inject
async def on_start_shift_car_wash(
        callback_query: CallbackQuery,
        callback_data: ShiftStartCarWashCallbackData,
        state: FSMContext,
        config: Config,
        shift_repository: ShiftRepository = Depends(
            dependency=get_shift_repository,
            use_cache=False,
        ),
) -> None:
    state_data: dict = await state.get_data()
    await state.clear()
    if (shift_date := state_data.get('date')) is not None:
        await shift_repository.create(
            staff_id=callback_query.from_user.id,
            car_wash_id=callback_data.car_wash_id,
            dates=[datetime.date.fromisoformat(shift_date)],
            immediate_start=True,
            is_extra=state_data.get('is_extra', False),
        )
    else:
        shift_id: int = state_data['shift_id']
        await shift_repository.start(
            shift_id=shift_id,
            car_wash_id=callback_data.car_wash_id,
        )
    await callback_query.message.edit_text(
        text='✅ Вы начали смену водителя перегонщика на мойку',
    )
    view = ShiftMenuView(
        staff_id=callback_query.from_user.id,
        web_app_base_url=config.web_app_base_url,
    )
    await answer_view(callback_query.message, view)

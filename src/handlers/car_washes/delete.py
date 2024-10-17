from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from fast_depends import inject, Depends

from callback_data import CarWashActionCallbackData
from callback_data.prefixes import CallbackDataPrefix
from dependencies.repositories import get_car_wash_repository
from enums import CarWashAction
from filters import admins_filter
from repositories import CarWashRepository
from states import CarWashDeleteStates
from views.base import answer_view, edit_message_by_view
from views.car_washes import CarWashListView, CarWashDeleteConfirmView

__all__ = ('router',)

router = Router(name=__name__)


@router.callback_query(
    F.data == CallbackDataPrefix.CAR_WASH_DELETE_CONFIRM,
    admins_filter,
    StateFilter('*')
)
@inject
async def on_car_wash_delete_confirm(
        callback_query: CallbackQuery,
        state: FSMContext,
        car_wash_repository: CarWashRepository = Depends(
            dependency=get_car_wash_repository,
            use_cache=False,
        ),
) -> None:
    state_data: dict = await state.get_data()
    car_wash_id: int = state_data['car_wash_id']
    await state.clear()
    await car_wash_repository.delete_by_id(car_wash_id)
    await callback_query.message.edit_text('❗️ Мойка удалена')
    car_washes = await car_wash_repository.get_all()
    view = CarWashListView(car_washes)
    await answer_view(callback_query.message, view)


@router.callback_query(
    CarWashActionCallbackData.filter(F.action == CarWashAction.DELETE),
    admins_filter,
    StateFilter('*')
)
async def on_start_delete_car_wash(
        callback_query: CallbackQuery,
        callback_data: CarWashActionCallbackData,
        state: FSMContext,
) -> None:
    await state.set_state(CarWashDeleteStates.confirm)
    await state.update_data(car_wash_id=callback_data.car_wash_id)
    view = CarWashDeleteConfirmView(callback_data.car_wash_id)
    await edit_message_by_view(callback_query.message, view)

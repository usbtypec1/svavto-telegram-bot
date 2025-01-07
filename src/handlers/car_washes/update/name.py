from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from fast_depends import inject, Depends

from callback_data import CarWashActionCallbackData
from callback_data.prefixes import CallbackDataPrefix
from config import Config
from dependencies.repositories import get_car_wash_repository
from enums import CarWashAction
from filters import admins_filter
from repositories import CarWashRepository
from states import CarWashRenameStates
from ui.views import edit_message_by_view, answer_text_view
from ui.views import (
    CarWashUpdateNameInputView,
    CarWashRenameConfirmView,
    CarWashDetailView,
)

__all__ = ('router',)

router = Router(name=__name__)


@router.callback_query(
    admins_filter,
    F.data == CallbackDataPrefix.CAR_WASH_UPDATE_CONFIRM,
    StateFilter(CarWashRenameStates.confirm),
)
@inject
async def on_car_wash_rename_confirmed(
        callback_query: CallbackQuery,
        state: FSMContext,
        config: Config,
        car_wash_repository: CarWashRepository = Depends(
            dependency=get_car_wash_repository,
            use_cache=False,
        ),
) -> None:
    state_data: dict = await state.get_data()
    await state.clear()
    car_wash_id: int = state_data['car_wash_id']
    car_wash_name: str = state_data['car_wash_name']
    await car_wash_repository.update(
        car_wash_id=car_wash_id,
        name=car_wash_name,
    )
    await callback_query.message.edit_text('✅ Название мойки обновлено')
    car_wash = await car_wash_repository.get_by_id(car_wash_id)
    view = CarWashDetailView(car_wash, config.web_app_base_url)
    await answer_text_view(callback_query.message, view)


@router.message(
    F.text,
    admins_filter,
    StateFilter(CarWashRenameStates.name),
)
async def on_car_wash_name_entered(
        message: Message,
        state: FSMContext,
) -> None:
    car_wash_name = message.text
    await state.set_state(CarWashRenameStates.confirm)
    await state.update_data(car_wash_name=car_wash_name)
    state_data: dict = await state.get_data()
    car_wash_id: int = state_data['car_wash_id']
    view = CarWashRenameConfirmView(
        car_wash_id=car_wash_id,
        car_wash_name=car_wash_name,
    )
    await answer_text_view(message, view)


@router.callback_query(
    admins_filter,
    CarWashActionCallbackData.filter(F.action == CarWashAction.RENAME),
    StateFilter('*'),
)
async def on_start_car_wash_rename_flow(
        callback_query: CallbackQuery,
        callback_data: CarWashActionCallbackData,
        state: FSMContext,
):
    view = CarWashUpdateNameInputView(
        car_wash_id=callback_data.car_wash_id,
    )
    await state.set_state(CarWashRenameStates.name)
    await state.update_data(car_wash_id=callback_data.car_wash_id)
    await edit_message_by_view(callback_query.message, view)

import asyncio

from aiogram import Bot, F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from fast_depends import inject

from callback_data import (
    ShiftRegularRejectCallbackData, ShiftRegularStartCallbackData,
    ShiftStartCarWashCallbackData,
)
from config import Config
from dependencies.repositories import (
    CarWashRepositoryDependency, ShiftRepositoryDependency,
)
from enums import ShiftType
from filters import admins_filter, staff_filter
from models import ShiftsConfirmation
from states import ShiftRegularStartStates
from ui.views import (
    ButtonText, ShiftMenuView, ShiftRegularStartRequestView,
    ShiftStartCarWashChooseView, ShiftStartForSpecificDateRequestSentView,
    TestShiftStartRequestView,
    answer_text_view, edit_as_rejected, edit_message_by_view, send_text_view,
)

__all__ = ('router',)

router = Router(name=__name__)


@router.callback_query(
    ShiftRegularRejectCallbackData.filter(),
    staff_filter,
)
async def on_shift_regular_start_reject(
        callback_query: CallbackQuery,
) -> None:
    await callback_query.answer('Вы отменили начало смены', show_alert=True)
    await edit_as_rejected(callback_query.message)


@router.callback_query(
    ShiftStartCarWashCallbackData.filter(),
    staff_filter,
    StateFilter(ShiftRegularStartStates.car_wash),
)
@inject
async def on_car_wash_choose(
        callback_query: CallbackQuery,
        callback_data: ShiftStartCarWashCallbackData,
        state: FSMContext,
        config: Config,
        shift_repository: ShiftRepositoryDependency,
) -> None:
    state_data: dict = await state.get_data()
    shift_id: int = state_data['shift_id']
    car_wash_id = callback_data.car_wash_id

    await shift_repository.start(
        shift_id=shift_id,
        car_wash_id=car_wash_id,
    )
    await callback_query.message.edit_text(
        text='✅ Вы начали смену водителя перегонщика на мойку',
    )
    view = ShiftMenuView(
        staff_id=callback_query.from_user.id,
        web_app_base_url=config.web_app_base_url,
    )
    await answer_text_view(callback_query.message, view)
    await callback_query.answer()


@router.callback_query(
    ShiftRegularStartCallbackData.filter(),
    staff_filter,
    StateFilter('*'),
)
@inject
async def on_shift_regular_start_accept(
        callback_query: CallbackQuery,
        callback_data: ShiftRegularStartCallbackData,
        car_wash_repository: CarWashRepositoryDependency,
        state: FSMContext,
) -> None:
    car_washes = await car_wash_repository.get_all()
    if not car_washes:
        await callback_query.answer(
            text='❌ Нет доступных моек',
            show_alert=True,
        )
        return
    await state.update_data(shift_id=callback_data.shift_id)
    await state.set_state(ShiftRegularStartStates.car_wash)
    view = ShiftStartCarWashChooseView(car_washes)
    await edit_message_by_view(callback_query.message, view)


@router.message(
    F.web_app_data.button_text == ButtonText.SHIFTS_FOR_SPECIFIC_DATE,
    admins_filter,
    StateFilter('*'),
)
@inject
async def on_send_shift_start_request_for_specific_date(
        message: Message,
        bot: Bot,
        shift_repository: ShiftRepositoryDependency,
) -> None:
    shifts_confirmation = ShiftsConfirmation.model_validate_json(
        json_data=message.web_app_data.data,
    )
    staff_ids = [staff.id for staff in shifts_confirmation.staff_list]
    shifts_page = await shift_repository.get_list(
        staff_ids=staff_ids,
        from_date=shifts_confirmation.date,
        to_date=shifts_confirmation.date,
        limit=1000,
        shift_types=(ShiftType.REGULAR,),
    )
    shifts = shifts_page.shifts

    staff_id_to_shift = {shift.staff.id: shift for shift in shifts}

    sent_message = await message.answer('Отправляю запросы на начало смены')

    for staff in shifts_confirmation.staff_list:
        try:
            shift = staff_id_to_shift[staff.id]
        except KeyError:
            view = TestShiftStartRequestView(date=shifts_confirmation.date)
        else:
            view = ShiftRegularStartRequestView(
                shift_id=shift.id,
                shift_date=shift.date,
                staff_full_name=shift.staff.full_name,
            )
        await send_text_view(bot, view, staff.id)
        await asyncio.sleep(0.1)

    view = ShiftStartForSpecificDateRequestSentView(
        staff_list=shifts_confirmation.staff_list,
    )
    await edit_message_by_view(sent_message, view)

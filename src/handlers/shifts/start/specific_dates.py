import asyncio

from aiogram import Bot, F, Router
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery, Message
from fast_depends import inject

from callback_data import (
    ShiftRegularStartCallbackData,
)
from dependencies.repositories import (
    CarWashRepositoryDependency, ShiftRepositoryDependency,
)
from enums import ShiftType
from filters import admins_filter, staff_filter
from interactors import (
    CarWashesReadInteractor,
    ShiftsOfStaffForPeriodReadInteractor,
)
from models import ShiftsConfirmation
from ui.views import (
    ButtonText, edit_message_by_view,
    ExtraShiftStartRequestView, send_text_view, ShiftCarWashUpdateView,
    ShiftRegularStartRequestView,
    ShiftStartForSpecificDateRequestSentView, TestShiftStartRequestView,
)


__all__ = ('router',)

router = Router(name=__name__)


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
        shift_repository: ShiftRepositoryDependency,
) -> None:
    await shift_repository.start(shift_id=callback_data.shift_id)
    car_washes = await CarWashesReadInteractor(car_wash_repository).execute()
    view = ShiftCarWashUpdateView(car_washes)
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

    interactor = ShiftsOfStaffForPeriodReadInteractor(
        shift_repository=shift_repository,
        from_date=shifts_confirmation.date,
        to_date=shifts_confirmation.date,
        staff_ids=staff_ids,
        shift_types=(ShiftType.REGULAR, ShiftType.EXTRA),
    )
    shifts = await interactor.execute()

    staff_id_to_shift = {shift.staff_id: shift for shift in shifts}

    sent_message = await message.answer('Отправляю запросы на начало смены')

    for staff in shifts_confirmation.staff_list:
        shift = staff_id_to_shift.get(staff.id)
        if shift is None:
            view = TestShiftStartRequestView(date=shifts_confirmation.date)
        elif shift.type == ShiftType.EXTRA:
            view = ExtraShiftStartRequestView(date=shifts_confirmation.date)
        elif shift.type == ShiftType.REGULAR:
            view = ShiftRegularStartRequestView(
                shift_id=shift.id,
                shift_date=shift.date,
                staff_full_name=shift.staff_full_name,
            )
        else:
            continue
        await send_text_view(bot, view, staff.id)
        await asyncio.sleep(0.1)

    view = ShiftStartForSpecificDateRequestSentView(
        staff_list=shifts_confirmation.staff_list,
    )
    await edit_message_by_view(sent_message, view)

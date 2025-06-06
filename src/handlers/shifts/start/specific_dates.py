import asyncio

from aiogram import Bot, F, Router
from aiogram.filters import StateFilter
from aiogram.types import Message
from fast_depends import inject

from dependencies.repositories import (
    ShiftRepositoryDependency,
)
from enums import ShiftType
from filters import admins_filter
from interactors import (
    ShiftsOfStaffForPeriodReadInteractor,
)
from models import ShiftsConfirmation, StaffIdAndDate
from ui.views import (
    ButtonText, edit_message_by_view,
    send_text_view, ShiftConfirmRequestView,
    ShiftStartForSpecificDateRequestSentView,
)


__all__ = ('router',)

router = Router(name=__name__)


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
    sent_message = await message.answer('Отправляю запросы на начало смены')

    shifts_confirmation = ShiftsConfirmation.model_validate_json(
        json_data=message.web_app_data.data,
    )
    all_staff_ids = {staff.id for staff in shifts_confirmation.staff_list}

    interactor = ShiftsOfStaffForPeriodReadInteractor(
        shift_repository=shift_repository,
        from_date=shifts_confirmation.date,
        to_date=shifts_confirmation.date,
        staff_ids=all_staff_ids,
        shift_types=(ShiftType.REGULAR, ShiftType.EXTRA),
    )
    shifts = await interactor.execute()

    staff_ids_with_shifts = {shift.staff_id for shift in shifts}
    staff_ids_without_shifts = all_staff_ids - staff_ids_with_shifts

    for shift in shifts:
        view = ShiftConfirmRequestView(shift)
        await send_text_view(bot, view, shift.staff_id)
        await asyncio.sleep(0.1)

    shifts_to_create = [
        StaffIdAndDate(staff_id=staff_id, date=shifts_confirmation.date)
        for staff_id in staff_ids_without_shifts
    ]
    if shifts_to_create:
        created_extra_shifts_result = await shift_repository.create_extra(
            shifts_to_create
        )
    else:
        created_extra_shifts_result = None

    view = ShiftStartForSpecificDateRequestSentView(
        staff_list=shifts_confirmation.staff_list,
        existing_shifts=shifts,
        created_extra_shifts_result=created_extra_shifts_result,
    )
    await edit_message_by_view(sent_message, view)

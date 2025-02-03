from aiogram import Bot, F, Router
from aiogram.filters import StateFilter
from aiogram.types import Message
from fast_depends import Depends, inject

from callback_data import ShiftRegularStartCallbackData
from dependencies.repositories import get_shift_repository
from filters import admins_filter
from models import ShiftsConfirmation
from repositories import ShiftRepository
from ui.views import send_text_view
from ui.views import ButtonText
from ui.views import TestShiftStartRequestView, ShiftRegularStartRequestView

__all__ = ('router',)

router = Router(name=__name__)


@router.callback_query(
ShiftRegularStartCallbackData.filter(),

    StateFilter('*'),
)
async def on_shift_regular_start_accept():
    pass


@router.message(
    F.web_app_data.button_text == ButtonText.SHIFTS_FOR_SPECIFIC_DATE,
    admins_filter,
    StateFilter('*'),
)
@inject
async def on_send_shift_start_request_for_specific_date(
        message: Message,
        bot: Bot,
        shift_repository: ShiftRepository = Depends(
            dependency=get_shift_repository,
            use_cache=False,
        ),
) -> None:
    shifts_confirmation = ShiftsConfirmation.model_validate_json(
        json_data=message.web_app_data.data,
    )
    shifts_page = await shift_repository.get_list(
        staff_ids=shifts_confirmation.staff_ids,
        limit=1000,
    )
    shifts = shifts_page.shifts

    staff_id_to_shift = {shift.staff.id: shift for shift in shifts}

    sent_message = await message.answer('Отправляю запросы на начало смены')

    count = 0
    for staff_id in shifts_confirmation.staff_ids:
        try:
            shift = staff_id_to_shift[staff_id]
        except KeyError:
            view = TestShiftStartRequestView(date=shifts_confirmation.date)
        else:
            view = ShiftRegularStartRequestView(
                shift_id=shift.id,
                shift_date=shift.date,
                staff_full_name=shift.staff.full_name,
            )
        finally:
            count += 1
        await send_text_view(bot, view, staff_id)

    await sent_message.edit_text(
        f'✅ Запросы на начало смены отправлены {count} сотрудникам',
    )

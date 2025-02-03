from aiogram import Bot, F, Router
from aiogram.filters import StateFilter
from aiogram.types import Message
from fast_depends import Depends, inject

from dependencies.repositories import get_shift_repository
from filters import admins_filter
from models import ShiftsConfirmation
from repositories import ShiftRepository
from ui.views import send_text_view
from ui.views import ButtonText
from ui.views import TestShiftStartRequestView, ShiftStartConfirmView

__all__ = ('router',)

router = Router(name=__name__)


@router.message(
    F.web_app_data.button_text == ButtonText.SHIFTS_TODAY,
    admins_filter,
    StateFilter('*'),
)
@inject
async def on_send_confirmation_to_staff(
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

    await message.answer('Отправляю запросы на начало смены')

    count = 0
    for staff_id in shifts_confirmation.staff_ids:
        try:
            shift = staff_id_to_shift[staff_id]
        except KeyError:
            view = TestShiftStartRequestView(date=shifts_confirmation.date)
        else:
            view = ShiftStartConfirmView(
                shift_id=shift.id,
                staff_full_name=shift.staff.full_name,
            )
        finally:
            count += 1
        await send_text_view(bot, view, staff_id)

    await message.answer(
        f'✅ Запросы на начало смены отправлены {count} сотрудникам',
    )

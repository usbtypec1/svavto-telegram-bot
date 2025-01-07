from aiogram import F, Router
from aiogram.filters import StateFilter, invert_f
from aiogram.types import Message
from fast_depends import Depends, inject

from dependencies.repositories import get_shift_repository
from exceptions import StaffHasNoAnyShiftError
from filters import admins_filter
from repositories import ShiftRepository
from ui.views import answer_text_view
from ui.views import ButtonText

__all__ = ('router',)

from ui.views import (
    StaffHasNoAnyCreatedShiftView,
    StaffScheduleCreatedShiftView,
)

router = Router(name=__name__)


@router.message(
    F.text == ButtonText.SCHEDULE_SELF,
    invert_f(admins_filter),
    StateFilter('*'),
)
@inject
async def on_show_schedule_self(
        message: Message,
        shift_repository: ShiftRepository = Depends(
            dependency=get_shift_repository,
            use_cache=False,
        ),
) -> None:
    try:
        shift_dates = await shift_repository.get_last_created_shift_dates(
            staff_id=message.from_user.id,
        )
    except StaffHasNoAnyShiftError:
        view = StaffHasNoAnyCreatedShiftView()
    else:
        view = StaffScheduleCreatedShiftView(shift_dates)
    await answer_text_view(message, view)

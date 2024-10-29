from aiogram import Router
from aiogram.filters import ExceptionTypeFilter

from aiogram.types import ErrorEvent

from exceptions import StaffHasNoActiveShiftError
from services.telegram_events import answer_appropriate_event

__all__ = ('router',)

router = Router(name=__name__)


@router.error(ExceptionTypeFilter(StaffHasNoActiveShiftError))
async def on_staff_has_no_active_shift_error(event: ErrorEvent) -> None:
    await answer_appropriate_event(event, 'Вы не начинали смену')

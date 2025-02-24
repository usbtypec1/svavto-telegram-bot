from aiogram import Router
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import ErrorEvent

from exceptions import (
    ShiftDateExpiredError, ShiftDateHasNotComeError,
    StaffHasActiveShiftError,
)


__all__ = ('router',)

router = Router(name=__name__)


@router.error(ExceptionTypeFilter(StaffHasActiveShiftError))
async def on_staff_has_active_shift_error(event: ErrorEvent) -> None:
    text = '❌ У вас уже есть активная смена'
    if event.update.callback_query is not None:
        await event.update.callback_query.answer(
            text=text,
            show_alert=True,
        )


@router.error(ExceptionTypeFilter(ShiftDateExpiredError))
async def on_shift_date_expired_error(event: ErrorEvent) -> None:
    text = f'❌ Вы не можете начать запланированную в прошлом смену'
    if event.update.callback_query is not None:
        await event.update.callback_query.answer(
            text=text,
            show_alert=True,
        )


@router.errors(ExceptionTypeFilter(ShiftDateHasNotComeError))
async def on_shift_date_has_not_come_error(event: ErrorEvent) -> None:
    error: ShiftDateHasNotComeError = event.exception
    text = f'❌ Вы сможете начать только в {error.shift_date:%d.%m.%Y}'
    if event.update.callback_query is not None:
        await event.update.callback_query.answer(
            text=text,
            show_alert=True,
        )

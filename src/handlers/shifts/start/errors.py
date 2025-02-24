import datetime

from aiogram import Router
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import ErrorEvent

from exceptions import (
    InvalidTimeToStartShiftError,
    ShiftAlreadyFinishedError,
    ShiftDateExpiredError,
    ShiftDateHasNotComeError,
    ShiftNotConfirmedError, StaffHasActiveShiftError,
)
from services.telegram_events import answer_appropriate_event
from ui.views import answer_view, ShiftTodayStartInvalidTimeView


__all__ = ('router',)

router = Router(name=__name__)


@router.error(ExceptionTypeFilter(ShiftAlreadyFinishedError))
async def on_shift_already_finished_error(event: ErrorEvent) -> None:
    shift_date = datetime.date.fromisoformat(event.exception.shift_date)
    text = f'❌ Смена на {shift_date:%d.%m.%Y} уже завершена'
    await answer_appropriate_event(event, text)


@router.error(ExceptionTypeFilter(InvalidTimeToStartShiftError))
async def on_invalid_time_to_start_shift_error(event: ErrorEvent) -> None:
    view = ShiftTodayStartInvalidTimeView()
    if event.update.callback_query is not None:
        await answer_view(
            event.update.callback_query.message,
            view,
        )


@router.error(ExceptionTypeFilter(ShiftNotConfirmedError))
async def on_shift_not_confirmed_error(event: ErrorEvent) -> None:
    text = '❌ Вы не подтвердили выход на смену'
    if event.update.callback_query is not None:
        await event.update.callback_query.answer(
            text=text,
            show_alert=True,
        )


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

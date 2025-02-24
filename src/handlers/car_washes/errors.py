from aiogram import Router
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import ErrorEvent

from exceptions import NoAnyCarWashError
from services.telegram_events import answer_appropriate_event


__all__ = ('router',)

router = Router(name=__name__)


@router.error(ExceptionTypeFilter(NoAnyCarWashError))
async def on_no_any_car_wash_error(event: ErrorEvent) -> None:
    await answer_appropriate_event(event, '❌ Нет доступных моек')

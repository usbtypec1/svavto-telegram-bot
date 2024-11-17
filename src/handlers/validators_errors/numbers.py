from aiogram import Router
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import ErrorEvent

from exceptions import InvalidNumberError
from services.telegram_events import answer_appropriate_event

__all__ = ('router',)

router = Router(name=__name__)


@router.error(ExceptionTypeFilter(InvalidNumberError))
async def on_invalid_number_error(event: ErrorEvent) -> None:
    # noinspection PyTypeChecker
    exception: InvalidNumberError = event.exception

    await answer_appropriate_event(
        event=event,
        text=f'❌ {exception.number} не является числом',
    )

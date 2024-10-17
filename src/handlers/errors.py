from json import JSONDecodeError

from aiogram import Router
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import ErrorEvent

__all__ = ('router',)

router = Router(name='global_errors')


@router.error(ExceptionTypeFilter(JSONDecodeError))
async def on_json_decode_error(event: ErrorEvent) -> None:
    if event.update.message is not None:
        await event.update.message.reply(
            text='Не получилось декодировать данные с сервера',
        )
    if event.update.callback_query is not None:
        await event.update.callback_query.answer(
            text='Не получилось декодировать данные с сервера',
            show_alert=True,
        )

from json import JSONDecodeError

from aiogram import Router
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import ErrorEvent

from exceptions import ServerApiError
from logger import create_logger

__all__ = ('router',)

router = Router(name='global_errors')
logger = create_logger('global_errors')


@router.error(ExceptionTypeFilter(ServerApiError))
async def on_server_api_error(event: ErrorEvent) -> None:
    if event.update.message is not None:
        logger.error(
            'Server API error',
            exc_info=event.exception,
        )
        await event.update.message.reply(
            text='Ошибка API сервера',
        )
    if event.update.callback_query is not None:
        logger.error(
            'Server API error',
            exc_info=event.exception,
        )
        await event.update.callback_query.answer(
            text='Ошибка API сервера',
            show_alert=True,
        )


@router.error(ExceptionTypeFilter(JSONDecodeError))
async def on_json_decode_error(event: ErrorEvent) -> None:
    if event.update.message is not None:
        logger.error(
            'Failed to decode JSON data from server',
            exc_info=event.exception,
        )
        await event.update.message.reply(
            text='Не получилось декодировать данные с сервера',
        )
    if event.update.callback_query is not None:
        logger.error(
            'Failed to decode JSON data from server',
            exc_info=event.exception,
        )
        await event.update.callback_query.answer(
            text='Не получилось декодировать данные с сервера',
            show_alert=True,
        )

from json import JSONDecodeError

import httpx
from aiogram import Router
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import ErrorEvent

from exceptions import ServerApiError, ShiftAlreadyExistsError
from logger import create_logger

__all__ = ('router',)

from services.telegram_events import answer_appropriate_event

router = Router(name='global_errors')
logger = create_logger('global_errors')

@router.error(ExceptionTypeFilter(ShiftAlreadyExistsError))
async def on_shift_already_exists_error(event: ErrorEvent) -> None:
    await answer_appropriate_event(
        event=event,
        text='❌ У вас уже есть смена на эту дату',
    )


@router.error(ExceptionTypeFilter(httpx.ConnectError))
async def on_connect_error(event: ErrorEvent) -> None:
    if event.update.message is not None:
        logger.error(
            'Connection error',
            exc_info=event.exception,
        )
        await event.update.message.reply(
            text='Ошибка подключения к серверу',
        )
    if event.update.callback_query is not None:
        logger.error(
            'Connection error',
            exc_info=event.exception,
        )
        await event.update.callback_query.answer(
            text='Ошибка подключения к серверу',
            show_alert=True,
        )


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

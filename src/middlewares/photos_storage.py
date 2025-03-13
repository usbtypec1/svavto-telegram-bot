import logging
from collections.abc import Awaitable, Callable
from typing import Any

from aiogram.types import Update
from redis.asyncio import Redis

from services.photos_storage import PhotosStorage


logger = logging.getLogger(__name__)


def photos_storage_middleware(
        handler: Callable[[Update, dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: dict[str, Any],
):
    redis: Redis = data['redis']
    if event.message is not None:
        user_id = event.message.from_user.id
    elif event.callback_query is not None:
        user_id = event.callback_query.from_user.id
    else:
        logger.warning('Unknown event type %s', event)
        return handler(event, data)

    data['photos_storage'] = PhotosStorage(redis=redis, user_id=user_id)
    return handler(event, data)

from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import Bot
from aiogram.types import Update
from fast_depends import Depends, inject

from dependencies.repositories import get_staff_repository
from exceptions import StaffNotFoundError
from repositories import StaffRepository
from services.telegram_events import get_user_id_from_update
from views.base import send_text_view
from views.menu import StaffBannedView

__all__ = ('banned_staff_middleware',)


@inject
async def banned_staff_middleware(
        handler: Callable[[Update, dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: dict[str, Any],
        staff_repository: StaffRepository = Depends(
            get_staff_repository,
            use_cache=False,
        ),
):
    bot: Bot = data['bot']
    data['staff'] = None

    try:
        user_id = get_user_id_from_update(event)
    except ValueError:
        return

    if user_id in data['admin_user_ids']:
        return await handler(event, data)

    try:
        staff = await staff_repository.get_by_id(user_id)
    except StaffNotFoundError:
        return await handler(event, data)

    if staff.is_banned:
        await send_text_view(bot, StaffBannedView(), user_id)
        return

    data['staff'] = staff

    return await handler(event, data)

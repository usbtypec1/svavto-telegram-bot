import datetime
from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Update
from fast_depends import Depends, inject

from dependencies.repositories import get_staff_repository
from logger import create_logger
from repositories import StaffRepository

__all__ = ('AdminUserIdsMiddleware',)

logger = create_logger('admins_middleware')


class AdminUserIdsMiddleware(BaseMiddleware):

    def __init__(self, *, ttl_in_seconds: int):
        self.__ttl_in_seconds = ttl_in_seconds
        self.__updated_at: datetime.datetime | None = None
        self.__admin_user_ids: set[int] | None = None

    async def __update_admin_user_ids(
            self,
            staff_repository: StaffRepository,
    ) -> None:
        self.__admin_user_ids = await staff_repository.get_all_admin_user_ids()
        self.__updated_at = datetime.datetime.now(datetime.UTC)

    def __is_expired(self) -> bool:
        if self.__updated_at is None:
            return True
        expires_at = self.__updated_at + datetime.timedelta(
            seconds=self.__ttl_in_seconds,
        )
        return datetime.datetime.now(datetime.UTC) > expires_at

    @inject
    async def __get_admin_user_ids(
            self,
            staff_repository: StaffRepository = Depends(
                dependency=get_staff_repository,
                use_cache=False,
            ),
    ) -> set[int]:
        if self.__admin_user_ids is None or self.__is_expired():
            logger.debug('Updating admin user ids')
            await self.__update_admin_user_ids(staff_repository)
        return self.__admin_user_ids

    async def __call__(
            self,
            handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
            event: Update,
            data: dict[str, Any],
    ):
        admin_user_ids = await self.__get_admin_user_ids()
        data['admin_user_ids'] = admin_user_ids
        return await handler(event, data)

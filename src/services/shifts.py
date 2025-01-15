import datetime
from typing import Protocol
from zoneinfo import ZoneInfo

from redis.asyncio import Redis

from exceptions import ShiftFinishPhotosCountExceededError

__all__ = (
    'get_current_shift_date',
    'ShiftFinishPhotosState',
    'is_time_to_start_shift',
)


class HasIdAndDate(Protocol):
    id: int
    date: datetime.date


def get_current_shift_date(timezone: ZoneInfo) -> datetime.date:
    """
    The **shift date** is the date when the shift was scheduled to start.
    Since the shift begins at 10 PM and ends at 7 AM,
    it technically spans two calendar days.
    However, the shift date is considered to be the date of its starting moment.

    Args:
        timezone: Timezone of place the car wash is located in.

    Returns:
        The date of the shift.
    """
    now = datetime.datetime.now(timezone)
    if now.hour <= 12:
        previous_day = now - datetime.timedelta(days=1)
        return previous_day.date()
    return now.date()


class ShiftFinishPhotosState:

    def __init__(self, *, redis: Redis, user_id: int):
        self.__redis = redis
        self.__user_id = user_id

    @property
    def key(self) -> str:
        return f'shift_finish_photos:{self.__user_id}'

    async def add_photo_file_id(self, photo_file_id: str) -> None:
        photo_file_ids_count = await self.get_photo_file_ids_count()
        if photo_file_ids_count > 10:
            raise ShiftFinishPhotosCountExceededError
        await self.__redis.sadd(self.key, photo_file_id)
        await self.__redis.expire(self.key, 60 * 60 * 24)

    async def clear(self) -> None:
        await self.__redis.delete(self.key)

    async def get_photo_file_ids(self) -> set[str]:
        return await self.__redis.smembers(self.key)

    async def delete_photo_file_id(self, photo_file_id: str) -> None:
        await self.__redis.srem(self.key, photo_file_id)

    async def get_photo_file_ids_count(self) -> int:
        return await self.__redis.scard(self.key)


def is_time_to_start_shift(timezone: ZoneInfo) -> bool:
    now = datetime.datetime.now(timezone)
    return now >= now.replace(hour=21, minute=30, second=0, microsecond=0)

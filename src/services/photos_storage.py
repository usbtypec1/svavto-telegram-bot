from dataclasses import dataclass

import redis.asyncio as redis


@dataclass(frozen=True, slots=True, kw_only=True)
class PhotosStorage:
    redis: redis.Redis
    user_id: int

    async def add_file_id(self, file_id: str) -> None:
        key = f'photos_storage:{self.user_id}'
        await self.redis.sadd(key, file_id)
        await self.redis.expire(key, 60 * 60 * 24)

    async def clear(self) -> None:
        key = f'photos_storage:{self.user_id}'
        await self.redis.delete(key)

    async def get_file_ids(self) -> set[str]:
        key = f'photos_storage:{self.user_id}'
        return await self.redis.smembers(key)

    async def delete_file_id(self, file_id: str) -> None:
        key = f'photos_storage:{self.user_id}'
        await self.redis.srem(key, file_id)

    async def count(self) -> int:
        key = f'photos_storage:{self.user_id}'
        return await self.redis.scard(key)

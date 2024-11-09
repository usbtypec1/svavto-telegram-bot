import httpx

from connections.base import ApiConnection

__all__ = ('AvailableDateConnection',)


class AvailableDateConnection(ApiConnection):

    async def get_all(self) -> httpx.Response:
        return await self._http_client.get('/shifts/available-dates/')

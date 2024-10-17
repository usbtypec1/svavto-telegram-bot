import httpx

from connections.base import ApiConnection

__all__ = ('CarWashConnection',)


class CarWashConnection(ApiConnection):

    async def get_all(self) -> httpx.Response:
        url = '/car-washes/'
        return await self._http_client.get(url)

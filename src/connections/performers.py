import httpx

from connections.base import ApiConnection

__all__ = ('PerformerConnection',)


class PerformerConnection(ApiConnection):

    async def get_by_id(self, user_id: int) -> httpx.Response:
        url = f'/performers/{user_id}/'
        return await self._http_client.get(url)

    async def create(
            self,
            user_id: int,
            full_name: str,
            car_sharing_phone_number: str,
            console_phone_number: str,
    ) -> httpx.Response:
        url = '/performers/'
        request_data = {
            'telegram_id': user_id,
            'full_name': full_name,
            'car_sharing_phone_number': car_sharing_phone_number,
            'console_phone_number': console_phone_number,
        }
        return await self._http_client.post(url, json=request_data)

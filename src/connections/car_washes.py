import httpx

from connections.base import ApiConnection
from logger import create_logger

__all__ = ('CarWashConnection',)

logger = create_logger('connections')


class CarWashConnection(ApiConnection):

    async def get_all(self) -> httpx.Response:
        url = '/car-washes/'
        logger.debug('Retrieving all car washes')
        response = await self._http_client.get(url)
        logger.debug(
            'Retrieved all car washes',
            extra={'status_code': response.status_code},
        )
        return response

    async def create(self, name: str) -> httpx.Response:
        url = '/car-washes/'
        logger.debug('Creating a car wash')
        response = await self._http_client.post(url, json={'name': name})
        logger.debug(
            'Created a car wash',
            extra={'status_code': response.status_code},
        )
        return response

    async def get_by_id(self, car_wash_id: int) -> httpx.Response:
        url = f'/car-washes/{car_wash_id}/'
        logger.debug('Retrieving a car wash by id')
        response = await self._http_client.get(url)
        logger.debug(
            'Retrieved a car wash by id',
            extra={'status_code': response.status_code},
        )
        return response

    async def update(self, *, car_wash_id: int, name: str) -> httpx.Response:
        url = f'/car-washes/{car_wash_id}/'
        logger.debug('Updating a car wash')
        response = await self._http_client.put(url, json={'name': name})
        logger.debug(
            'Updated a car wash',
            extra={'status_code': response.status_code},
        )
        return response

    async def delete_by_id(self, car_wash_id: int) -> httpx.Response:
        url = f'/car-washes/{car_wash_id}/'
        logger.debug('Deleting a car wash')
        response = await self._http_client.delete(url)
        logger.debug(
            'Deleted a car wash',
            extra={'status_code': response.status_code},
        )
        return response

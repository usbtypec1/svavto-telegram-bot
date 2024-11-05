import datetime

import httpx

from connections.base import ApiConnection
from logger import create_logger
from models import CarToWashWebAppData

__all__ = ('CarToWashConnection',)

logger = create_logger('connections')


class CarToWashConnection(ApiConnection):

    async def create(
            self,
            *,
            staff_id: int,
            car_to_wash: CarToWashWebAppData,
    ) -> httpx.Response:
        url = '/shifts/cars/'
        request_data = car_to_wash.model_dump() | {'staff_id': staff_id}
        logger.debug(
            'Adding car to wash',
            extra={'request_data': request_data}
        )
        response = await self._http_client.post(url, json=request_data)
        logger.debug(
            'Car to wash created',
            extra={'status_code': response.status_code}
        )
        return response

    async def get_all(self, staff_id: int) -> httpx.Response:
        url = f'/shifts/cars/staff/{staff_id}/'
        logger.debug(
            'Retrieving all cars added in shift',
            extra={'staff_id': staff_id},
        )
        response = await self._http_client.get(url)
        logger.debug(
            'Retrieved all cars added in shift',
            extra={'status_code': response.status_code},
        )
        return response

    async def update_additional_services(
            self,
            *,
            car_id: int,
            additional_services: list[dict],
    ) -> httpx.Response:
        url = f'/shifts/cars/{car_id}/'
        request_data = {
            'additional_services': additional_services,
        }
        return await self._http_client.patch(url, json=request_data)

    async def get_count_by_staff(
            self,
            date: datetime.date,
    ) -> httpx.Response:
        url = f'/shifts/cars/count-by-staff/'
        query_params = {'date': f'{date:%Y-%m-%d}'}
        return await self._http_client.get(url, params=query_params)

    async def get_without_windshield_washer(
            self,
            date: datetime.date,
    ) -> httpx.Response:
        url = f'/shifts/cars/without-windshield-washer/'
        query_params = {'date': f'{date:%Y-%m-%d}'}
        return await self._http_client.get(url, params=query_params)

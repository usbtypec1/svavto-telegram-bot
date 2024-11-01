import datetime

import httpx

from connections.base import ApiConnection
from logger import create_logger

__all__ = ('ShiftConnection',)

logger = create_logger('connections')


class ShiftConnection(ApiConnection):

    async def get_active(self, staff_id: int) -> httpx.Response:
        url = f'/shifts/current/{staff_id}/'
        logger.debug(
            f'Retrieving active shift for staff {staff_id}',
        )
        response = await self._http_client.get(url)
        logger.debug(
            f'Received active shift for staff {staff_id}',
            extra={'status_code': response.status_code},
        )
        return response

    async def update_current_shift_car_wash(
            self,
            *,
            staff_id: int,
            car_wash_id: int,
    ) -> httpx.Response:
        url = f'/shifts/current/{staff_id}/car-washes/'
        logger.debug(
            f'Updating current shift car wash to {car_wash_id}',
        )
        response = await self._http_client.patch(
            url,
            json={'car_wash_id': car_wash_id},
        )
        logger.debug(
            f'Updated current shift car wash to {car_wash_id}',
            extra={'status_code': response.status_code},
        )
        return response

    async def start(
            self,
            *,
            staff_id: int,
            date: datetime.date,
            car_wash_id: int,
    ) -> httpx.Response:
        url = '/shifts/start/'
        logger.debug(
            f'Starting shift for staff {staff_id}',
        )
        response = await self._http_client.post(
            url,
            json={
                'staff_id': staff_id,
                'date': f'{date:%Y-%m-%d}',
                'car_wash_id': car_wash_id,
            },
        )
        logger.debug(
            f'Started shift for staff {staff_id}',
            extra={'status_code': response.status_code},
        )
        return response

    async def finish(
            self,
            *,
            staff_id: int,
    ) -> httpx.Response:
        url = f'/shifts/finish/'
        logger.debug(
            f'Finishing shift for staff {staff_id}',
        )
        response = await self._http_client.post(url)
        logger.debug(
            f'Finished shift for staff {staff_id}',
            extra={'status_code': response.status_code},
        )
        return response

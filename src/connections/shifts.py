import datetime
from collections.abc import Iterable

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
            shift_id: int,
            car_wash_id: int,
    ) -> httpx.Response:
        url = '/shifts/start/'
        logger.debug(
            f'Starting shift {shift_id}',
        )
        response = await self._http_client.post(
            url,
            json={
                'shift_id': shift_id,
                'car_wash_id': car_wash_id,
            },
        )
        logger.debug(
            f'Started shift {shift_id}',
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
        request_data = {'staff_id': staff_id}
        response = await self._http_client.post(url, json=request_data)
        logger.debug(
            f'Finished shift for staff {staff_id}',
            extra={'status_code': response.status_code},
        )
        return response

    async def confirm(
            self,
            *,
            staff_id: int,
            date: datetime.date,
    ) -> httpx.Response:
        url = '/shifts/confirm/'
        logger.debug(
            f'Confirming shift for staff {staff_id}',
        )
        request_data = {
            'staff_id': staff_id,
            'date': f'{date:%Y-%m-%d}',
        }
        response = await self._http_client.post(url, json=request_data)
        logger.debug(
            f'Confirmed shift for staff {staff_id}',
            extra={'status_code': response.status_code},
        )
        return response

    async def get_shifts_by_staff_id(
            self,
            staff_id: int,
            month: int,
            year: int,
    ) -> httpx.Response:
        url = f'/shifts/staff/{staff_id}/'
        logger.debug(f'Retrieving shifts of staff {staff_id}')
        query_params = {'month': month, 'year': year}
        response = await self._http_client.get(url, params=query_params)
        logger.debug(
            f'Retrieved shifts of staff {staff_id}',
            extra={'status_code': response.status_code}
        )
        return response

    async def create(
            self,
            *,
            staff_id: int,
            dates: Iterable[datetime.date],
    ):
        url = '/shifts/create/'
        logger.debug(f'Creating shifts for staff {staff_id}')
        request_data = {
            'staff_id': staff_id,
            'dates': [f'{date:%Y-%m-%d}' for date in dates],
        }
        response = await self._http_client.post(url, json=request_data)
        logger.debug(
            f'Created shifts for staff {staff_id}',
            extra={'status_code': response.status_code},
        )
        return response

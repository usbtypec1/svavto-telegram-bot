import datetime
from collections.abc import Iterable

import httpx

from connections.base import ApiConnection
from logger import create_logger

__all__ = ('ShiftConnection',)

logger = create_logger('connections')


class ShiftConnection(ApiConnection):

    async def get_list(
            self,
            *,
            date_from: datetime.date | None = None,
            date_to: datetime.date | None = None,
            staff_ids: Iterable[int] | None = None,
            limit: int | None = None,
            offset: int | None = None,
    ) -> httpx.Response:
        url = '/shifts/'
        query_params = {}
        if date_from is not None:
            query_params['date_from'] = f'{date_from:%Y-%m-%d}'
        if date_to is not None:
            query_params['date_to'] = f'{date_to:%Y-%m-%d}'
        if staff_ids is not None:
            query_params['staff_ids'] = tuple(staff_ids)
        if limit is not None:
            query_params['limit'] = limit
        if offset is not None:
            query_params['offset'] = offset
        logger.debug('Retrieving shifts list')
        response = await self._http_client.get(url, params=query_params)
        logger.debug(
            'Received shifts list',
            extra={'status_code': response.status_code},
        )
        return response

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
            statement_photo_file_id: str,
            service_app_photo_file_id: str,
    ) -> httpx.Response:
        """
        Call API endpoint that finishes current shift of staff.

        Keyword Args:
            staff_id: Staff Telegram ID.
            statement_photo_file_id: File ID of photo of statement.
            service_app_photo_file_id: File ID of photo of service application.

        Returns:
            Response from the API.
        """
        url = f'/shifts/finish/'
        logger.debug(
            f'Finishing shift for staff {staff_id}',
        )
        request_data = {
            'staff_id': staff_id,
            'statement_photo_file_id': statement_photo_file_id,
            'service_app_photo_file_id': service_app_photo_file_id,
        }
        response = await self._http_client.post(url, json=request_data)
        logger.debug(
            f'Finished shift for staff {staff_id}',
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
            immediate_start: bool,
            car_wash_id: int | None,
            is_extra: bool,
    ) -> httpx.Response:
        url = '/shifts/create/'
        logger.debug(f'Creating shifts for staff {staff_id}')
        request_data = {
            'staff_id': staff_id,
            'dates': [f'{date:%Y-%m-%d}' for date in dates],
            'immediate_start': immediate_start,
            'car_wash_id': car_wash_id,
            'is_extra': is_extra,
        }
        response = await self._http_client.post(url, json=request_data)
        logger.debug(
            f'Created shifts for staff {staff_id}',
            extra={'status_code': response.status_code},
        )
        return response

    async def get_last_created_shift_dates(
            self,
            staff_id: int,
    ) -> httpx.Response:
        url = f'/shifts/staff/{staff_id}/last-created/'
        logger.debug(
            f'Retrieving last created shift dates for staff {staff_id}',
        )
        response = await self._http_client.get(url)
        logger.debug(
            f'Retrieved last created shift dates for staff {staff_id}',
            extra={'status_code': response.status_code},
        )
        return response

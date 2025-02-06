import datetime
from collections.abc import Iterable

import httpx

from connections.base import ApiConnection
from enums import ShiftType
from logger import create_logger

__all__ = ('ShiftConnection',)

logger = create_logger('connections')


class ShiftConnection(ApiConnection):

    async def get_by_id(self, shift_id: int) -> httpx.Response:
        url = f'/shifts/{shift_id}/'
        logger.debug(f'Retrieving shift {shift_id}')
        response = await self._http_client.get(url)
        logger.debug(
            f'Received shift {shift_id}',
            extra={'status_code': response.status_code},
        )
        return response

    async def get_list(
            self,
            *,
            from_date: datetime.date | None = None,
            to_date: datetime.date | None = None,
            staff_ids: Iterable[int] | None = None,
            limit: int | None = None,
            offset: int | None = None,
            shift_types: Iterable[ShiftType] | None = None,
    ) -> httpx.Response:
        url = '/shifts/v2/'
        query_params = {}
        if from_date is not None:
            query_params['date_from'] = f'{from_date:%Y-%m-%d}'
        if to_date is not None:
            query_params['date_to'] = f'{to_date:%Y-%m-%d}'
        if staff_ids is not None:
            query_params['staff_ids'] = tuple(staff_ids)
        if limit is not None:
            query_params['limit'] = limit
        if offset is not None:
            query_params['offset'] = offset
        if shift_types is not None:
            query_params['types'] = tuple(shift_types)
        logger.debug('Retrieving shifts list. Query params: %s', query_params)
        response = await self._http_client.get(url, params=query_params)
        logger.debug(
            'Received shifts list with status code %d',
            response.status_code,
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
            photo_file_ids: Iterable[str],
    ) -> httpx.Response:
        """
        Call API endpoint that finishes current shift of staff.

        Keyword Args:
            staff_id: Staff Telegram ID.
            photo_file_ids: File ID of photo of statement or service app.

        Returns:
            Response from the API.
        """
        url = f'/shifts/finish/'
        logger.debug(
            f'Finishing shift for staff {staff_id}',
        )
        request_data = {
            'staff_id': staff_id,
            'photo_file_ids': tuple(photo_file_ids),
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

    async def create_regular(
            self,
            *,
            staff_id: int,
            dates: Iterable[datetime.date],
    ) -> httpx.Response:
        url = '/shifts/create/'
        request_data = {
            'staff_id': staff_id,
            'dates': [f'{date:%Y-%m-%d}' for date in dates],
        }
        logger.debug(f'Creating regular shifts for staff %d', staff_id)
        response = await self._http_client.post(url, json=request_data)
        logger.debug(
            f'Created shifts for staff %d. Status code: %d',
            staff_id,
            response.status_code,
        )
        return response

    async def create_extra(
            self,
            *,
            staff_id: int,
            shift_date: datetime.date,
    ) -> httpx.Response:
        """
        Create extra shift for staff.

        Keyword Args:
            staff_id: Staff Telegram ID.
            shift_date: Date of the shift.

        Returns:
            Response from the API.
        """
        url = '/shifts/create/extra/'
        logger.debug(f'Creating extra shift for staff %d', staff_id)
        request_data = {
            'staff_id': staff_id,
            'date': f'{shift_date:%Y-%m-%d}',
        }
        response = await self._http_client.post(url, json=request_data)
        logger.debug(
            f'Created extra shift for staff %d. Status code: %d',
            staff_id,
            response.status_code,
        )
        return response

    async def create_test(
            self,
            *,
            staff_id: int,
            shift_date: datetime.date,
    ) -> httpx.Response:
        """
        Create test shift for staff.

        Keyword Args:
            staff_id: Staff Telegram ID.
            shift_date: Date of the shift.

        Returns:
            Response from the API.
        """
        url = '/shifts/create/test/'
        logger.debug(f'Creating test shift for staff %d', staff_id)
        request_data = {
            'staff_id': staff_id,
            'date': f'{shift_date:%Y-%m-%d}',
        }
        response = await self._http_client.post(url, json=request_data)
        logger.debug(
            f'Created test shift for staff %d. Status code: %d',
            staff_id,
            response.status_code,
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

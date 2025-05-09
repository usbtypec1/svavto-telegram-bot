import httpx

from connections.base import ApiConnection
from enums import StaffType
from logger import create_logger

__all__ = ('StaffConnection',)

logger = create_logger('connections')


class StaffConnection(ApiConnection):

    async def get_by_id(self, user_id: int) -> httpx.Response:
        logger.debug('Retrieving staff by id %d', user_id)
        url = f'/staff/{user_id}/'
        response = await self._http_client.get(url)
        logger.debug(
            'Retrieved staff by id %d. Status code: %d',
            user_id,
            response.status_code,
        )
        return response

    async def get_all(
            self,
            *,
            order_by: str,
            include_banned: bool,
            limit: int | None,
            offset: int | None,
    ) -> httpx.Response:
        url = '/staff/'
        query_params = {
            'order_by': order_by,
            'include_banned': include_banned,
        }
        if limit is not None:
            query_params['limit'] = limit
        if offset is not None:
            query_params['offset'] = offset
        logger.debug(
            'Retrieving all staff. Order by: %s, include banned: %s, limit: '
            '%s, offset: %s',
            order_by,
            include_banned,
            limit,
            offset,
        )
        response = await self._http_client.get(url, params=query_params)
        logger.debug(
            'Retrieved all staff. Status code: %d',
            response.status_code,
        )
        return response

    async def update_by_id(
            self,
            *,
            staff_id: int,
            is_banned: bool,
            staff_type: StaffType,
    ) -> httpx.Response:
        url = f'/staff/{staff_id}/'
        request_data = {'is_banned': is_banned, 'type': staff_type}
        logger.debug(
            'Updating staff with telegram id %d',
            staff_id,
        )
        response = await self._http_client.put(url, json=request_data)
        logger.debug(
            'Updated staff with telegram id %d. Status code:',
            staff_id,
            response.status_code,
        )
        return response

    async def get_all_admin_staff(self) -> httpx.Response:
        url = '/staff/admins/'
        logger.debug('Retrieving all admins')
        response = await self._http_client.get(url)
        logger.debug(
            'Retrieved all admins. Status code: %d',
            response.status_code,
        )
        return response

    async def create_register_request(
            self,
            *,
            staff_id: int,
            full_name: str,
            car_sharing_phone_number: str,
            console_phone_number: str,
            staff_type: int,
    ) -> httpx.Response:
        url = '/staff/register-requests/'
        request_data = {
            'staff_id': staff_id,
            'full_name': full_name,
            'car_sharing_phone_number': car_sharing_phone_number,
            'console_phone_number': console_phone_number,
            'staff_type': staff_type,
        }
        logger.debug(
            'Sending staff register request for staff ID: %d',
            staff_id,
        )
        response = await self._http_client.post(url, json=request_data)
        logger.debug(
            'Received staff register request for staff ID %d. Status code: %d',
            staff_id,
            response.status_code,
        )
        return response

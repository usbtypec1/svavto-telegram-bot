import httpx

from connections.base import ApiConnection
from logger import create_logger

__all__ = ('ShiftConnection',)

logger = create_logger('connections')


class ShiftConnection(ApiConnection):

    async def get_active(self, staff_id: int) -> httpx.Response:
        url = f'/shifts/staff/{staff_id}/'
        logger.debug(
            f'Retrieving active shift for staff {staff_id}',
        )
        response = await self._http_client.get(url)
        logger.debug(
            f'Received active shift for staff {staff_id}',
            extra={'status_code': response.status_code},
        )
        return response

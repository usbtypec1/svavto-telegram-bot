import httpx

from connections.base import ApiConnection
from logger import create_logger

__all__ = ('ShiftConnection',)

logger = create_logger('connections')


class ShiftConnection(ApiConnection):

    async def get_active(self, staff_id: int) -> httpx.Response:
        url = '/shifts/active/'
        query_params = {'staff_id': staff_id}
        logger.debug(
            f'Retrieving active shift for staff {staff_id}',
            extra={'query_params': query_params},
        )
        response = await self._http_client.get(url, params=query_params)
        logger.debug(
            f'Received active shift for staff {staff_id}',
            extra={'response': response},
        )
        return response

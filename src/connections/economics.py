import httpx

from connections.base import ApiConnection
from logger import create_logger

__all__ = ('EconomicsConnection',)

logger = create_logger('connections')


class EconomicsConnection(ApiConnection):

    async def create_penalty(
            self,
            *,
            staff_id: int,
            reason: str,
    ) -> httpx.Response:
        url = '/economics/penalties/'
        request_data = {
            'staff_id': staff_id,
            'reason': reason,
        }
        logger.debug(
            'Creating penalty',
            extra={'request_data': request_data},
        )
        response = await self._http_client.post(url, json=request_data)
        logger.debug(
            'Created penalty',
            extra={'status_code': response.status_code},
        )
        return response

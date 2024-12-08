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
            shift_id: int,
            reason: str,
            amount: int | None,
    ) -> httpx.Response:
        url = '/economics/penalties/'
        request_data = {
            'staff_id': staff_id,
            'shift_id': shift_id,
            'reason': reason,
        }
        if amount is not None:
            request_data['amount'] = amount
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

    async def create_surcharge(
            self,
            *,
            staff_id: int,
            shift_id: int,
            reason: str,
            amount: int,
    ) -> httpx.Response:
        url = '/economics/surcharges/'
        request_data = {
            'staff_id': staff_id,
            'shift_id': shift_id,
            'reason': reason,
            'amount': amount,
        }
        logger.debug(
            'Creating surcharge',
            extra={'request_data': request_data},
        )
        response = await self._http_client.post(url, json=request_data)
        logger.debug(
            'Created surcharge',
            extra={'status_code': response.status_code},
        )
        return response

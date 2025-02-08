import httpx

from connections.base import ApiConnection
from logger import create_logger

__all__ = ('EconomicsConnection',)

logger = create_logger('connections')


class EconomicsConnection(ApiConnection):

    async def create_penalty(
            self,
            *,
            shift_id: int,
            reason: str,
            amount: int | None,
    ) -> httpx.Response:
        url = '/economics/penalties/'
        request_data = {
            'shift_id': shift_id,
            'reason': reason,
        }
        if amount is not None:
            request_data['amount'] = amount
        logger.debug(
            'Sending create penalty request: data %s',
            request_data
        )
        response = await self._http_client.post(url, json=request_data)
        logger.debug(
            'Received create penalty response: status code %d',
            response.status_code
        )
        return response

    async def create_surcharge(
            self,
            *,
            shift_id: int,
            reason: str,
            amount: int,
    ) -> httpx.Response:
        url = '/economics/surcharges/'
        request_data = {
            'shift_id': shift_id,
            'reason': reason,
            'amount': amount,
        }
        logger.debug(
            'Sending create surcharge request: data %s',
            request_data
        )
        response = await self._http_client.post(url, json=request_data)
        logger.debug(
            'Received create surcharge response: status code %d',
            response.status_code
        )
        return response

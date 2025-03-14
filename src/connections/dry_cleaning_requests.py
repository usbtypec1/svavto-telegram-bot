from collections.abc import Iterable

import httpx

from connections.base import ApiConnection


class DryCleaningRequestConnection(ApiConnection):

    async def create(
            self,
            *,
            shift_id: int,
            car_number: str,
            photo_file_ids: Iterable[str],
            services: Iterable[dict],
    ) -> httpx.Response:
        url = '/dry-cleaning/requests/'
        request_data = {
            'shift_id': shift_id,
            'car_number': car_number,
            'photo_file_ids': tuple(photo_file_ids),
            'services': tuple(services),
        }
        response = await self._http_client.post(url, json=request_data)
        return response

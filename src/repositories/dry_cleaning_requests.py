from collections.abc import Iterable

from connections import DryCleaningRequestConnection
from models import DryCleaningRequest, DryCleaningRequestService


class DryCleaningRequestRepository:

    def __init__(self, connection: DryCleaningRequestConnection):
        self.__connection = connection

    async def create(
            self,
            *,
            shift_id: int,
            car_number: str,
            photo_file_ids: Iterable[str],
            services: Iterable[DryCleaningRequestService],
    ) -> DryCleaningRequest:
        services = [
            {
                'id': str(service.id),
                'count': service.count,
            }
            for service in services
        ]
        response = await self.__connection.create(
            shift_id=shift_id,
            car_number=car_number,
            photo_file_ids=photo_file_ids,
            services=services,
        )
        return DryCleaningRequest.model_validate_json(response.text)

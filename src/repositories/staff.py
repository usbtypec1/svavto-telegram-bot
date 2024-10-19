from pydantic import TypeAdapter

from connections import StaffConnection
from models import Staff, StaffToCreate
from repositories.errors import handle_errors
from logger import create_logger

__all__ = ('StaffRepository',)

logger = create_logger('repositories')


class StaffRepository:

    def __init__(self, connection: StaffConnection):
        self.__connection = connection

    async def get_by_id(self, user_id: int) -> Staff:
        response = await self.__connection.get_by_id(user_id)
        response_data = response.json()
        logger.info(
            'Decoded response data',
            extra={'response_data': response_data},
        )
        handle_errors(response)
        return Staff.model_validate(response_data)

    async def get_all(self) -> list[Staff]:
        response = await self.__connection.get_all()
        response_data = response.json()
        handle_errors(response)
        type_adapter = TypeAdapter(list[Staff])
        return type_adapter.validate_python(response_data['staff'])

    async def create(self, staff: StaffToCreate) -> Staff:
        response = await self.__connection.create(
            telegram_id=staff.id,
            full_name=staff.full_name,
            car_sharing_phone_number=staff.car_sharing_phone_number,
            console_phone_number=staff.console_phone_number,
        )
        response_data = response.json()
        logger.info(
            'Decoded staff create response JSON data',
            extra={'response_data': response_data},
        )
        handle_errors(response)
        return Staff.model_validate(response_data)

    async def update_by_telegram_id(
            self,
            *,
            telegram_id: int,
            is_banned: bool,
    ) -> None:
        response = await self.__connection.update_by_telegram_id(
            telegram_id=telegram_id,
            is_banned=is_banned,
        )
        handle_errors(response)

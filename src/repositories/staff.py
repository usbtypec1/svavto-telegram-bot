from pydantic import TypeAdapter

from connections import StaffConnection
from enums import StaffOrderBy
from logger import create_logger
from models import (
    Staff,
    StaffToRegisterWithId,
    StaffWithAvailableDates,
)
from repositories.errors import handle_errors

__all__ = ('StaffRepository',)

logger = create_logger('repositories')


class StaffRepository:

    def __init__(self, connection: StaffConnection):
        self.__connection = connection

    async def get_by_id(self, user_id: int) -> StaffWithAvailableDates:
        response = await self.__connection.get_by_id(user_id)
        response_data = response.json()
        logger.info(
            'Decoded response data',
            extra={'response_data': response_data},
        )
        handle_errors(response)
        return StaffWithAvailableDates.model_validate(response_data)

    async def get_all(self, *, order_by: StaffOrderBy) -> list[Staff]:
        response = await self.__connection.get_all(order_by=order_by)
        response_data = response.json()
        handle_errors(response)
        type_adapter = TypeAdapter(list[Staff])
        return type_adapter.validate_python(response_data['staff'])

    async def create(self, staff: StaffToRegisterWithId) -> None:
        response = await self.__connection.create(
            telegram_id=staff.id,
            full_name=staff.full_name,
            car_sharing_phone_number=staff.car_sharing_phone_number,
            console_phone_number=staff.console_phone_number,
        )
        handle_errors(response)

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

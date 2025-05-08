from connections import StaffConnection
from enums import StaffOrderBy
from logger import create_logger
from models import Staff, StaffListPage, StaffRegisterRequest
from repositories.errors import handle_errors

__all__ = ('StaffRepository',)

logger = create_logger('repositories')


class StaffRepository:

    def __init__(self, connection: StaffConnection):
        self.__connection = connection

    async def get_by_id(self, staff_id: int) -> Staff:
        response = await self.__connection.get_by_id(staff_id)
        response_data = response.json()
        logger.info(
            'Decoded response data',
            extra={'response_data': response_data},
        )
        handle_errors(response)
        return Staff.model_validate(response_data)

    async def get_all(
            self,
            *,
            order_by: StaffOrderBy,
            include_banned: bool = False,
            limit: int | None = None,
            offset: int | None = None,
    ) -> StaffListPage:
        response = await self.__connection.get_all(
            order_by=order_by,
            include_banned=include_banned,
            limit=limit,
            offset=offset,
        )
        handle_errors(response)
        return StaffListPage.model_validate_json(response.text)

    async def update_by_id(
            self,
            *,
            staff_id: int,
            is_banned: bool,
    ) -> None:
        response = await self.__connection.update_by_id(
            staff_id=staff_id,
            is_banned=is_banned,
        )
        handle_errors(response)

    async def get_all_admin_user_ids(self) -> set[int]:
        response = await self.__connection.get_all_admin_staff()
        handle_errors(response)
        response_data = response.json()
        return {
            staff['id']
            for staff in response_data['admin_staff']
        }

    async def create_register_request(
            self,
            *,
            staff_id: int,
            full_name: str,
            car_sharing_phone_number: str,
            console_phone_number: str,
            staff_type: int,
    ) -> StaffRegisterRequest:
        response = await self.__connection.create_register_request(
            staff_id=staff_id,
            full_name=full_name,
            car_sharing_phone_number=car_sharing_phone_number,
            console_phone_number=console_phone_number,
            staff_type=staff_type,
        )
        handle_errors(response)
        return StaffRegisterRequest.model_validate_json(response.text)

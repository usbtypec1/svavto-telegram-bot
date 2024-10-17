from connections import StaffConnection
from models import Performer
from repositories.errors import handle_errors

__all__ = ('StaffRepository',)


class StaffRepository:

    def __init__(self, connection: StaffConnection):
        self.__connection = connection

    async def get_user_by_id(self, user_id: int) -> Performer:
        response = await self.__connection.get_by_id(user_id)
        response_data = response.json()
        handle_errors(response)
        return Performer.model_validate(response_data)

    async def get_all(self) -> list[Performer]:
        response = await self.__connection.get_all()
        response_data = response.json()
        handle_errors(response)
        return [Performer.model_validate(item) for item in response_data]

    async def create(self, performer: Performer) -> Performer:
        response = await self.__connection.create(
            telegram_id=performer.telegram_id,
            full_name=performer.full_name,
            car_sharing_phone_number=performer.car_sharing_phone_number,
            console_phone_number=performer.console_phone_number,
        )
        response_data = response.json()
        handle_errors(response)
        return Performer.model_validate(response_data)

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

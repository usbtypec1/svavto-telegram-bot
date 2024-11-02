import datetime

from connections import ShiftConnection
from models import CarWash, ShiftFinishResult
from repositories.errors import handle_errors

__all__ = ('ShiftRepository',)


class ShiftRepository:

    def __init__(self, connection: ShiftConnection):
        self.__connection = connection

    async def get_active(self, staff_id: int):
        response = await self.__connection.get_active(staff_id)
        handle_errors(response)

    async def update_current_shift_car_wash(
            self,
            *,
            staff_id: int,
            car_wash_id: int,
    ) -> CarWash:
        response = await self.__connection.update_current_shift_car_wash(
            staff_id=staff_id,
            car_wash_id=car_wash_id,
        )
        handle_errors(response)
        response_data = response.json()
        return CarWash.model_validate(response_data)

    async def start(
            self,
            *,
            shift_id: int,
            car_wash_id: int,
    ) -> None:
        response = await self.__connection.start(
            shift_id=shift_id,
            car_wash_id=car_wash_id,
        )
        handle_errors(response)

    async def finish(
            self,
            *,
            staff_id: int,
    ) -> ShiftFinishResult:
        response = await self.__connection.finish(staff_id=staff_id)
        handle_errors(response)
        response_data = response.json()
        return ShiftFinishResult.model_validate(response_data)

    async def confirm(
            self,
            *,
            staff_id: int,
            date: datetime.date,
    ) -> None:
        response = await self.__connection.confirm(
            staff_id=staff_id,
            date=date,
        )
        handle_errors(response)

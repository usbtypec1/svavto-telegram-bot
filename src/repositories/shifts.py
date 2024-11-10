import datetime

from pydantic import TypeAdapter

from connections import ShiftConnection
from models import CarWash, Shift, ShiftCreateResult, ShiftFinishResult
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

    async def get_shifts_by_staff_id(
            self,
            *,
            staff_id: int,
            month: int,
            year: int,
    ) -> list[Shift]:
        response = await self.__connection.get_shifts_by_staff_id(
            staff_id=staff_id,
            month=month,
            year=year,
        )
        handle_errors(response)
        response_data = response.json()
        type_adapter = TypeAdapter(list[Shift])
        return type_adapter.validate_python(response_data['shifts'])

    async def create(
            self,
            *,
            staff_id: int,
            dates: list[datetime.date],
    ) -> ShiftCreateResult:
        response = await self.__connection.create(
            staff_id=staff_id,
            dates=dates,
        )
        handle_errors(response)
        response_data = response.json()
        return ShiftCreateResult.model_validate(response_data)

    async def get_last_created_shift_dates(
            self,
            staff_id: int,
    ) -> list[datetime.date]:
        response = await self.__connection.get_last_created_shift_dates(
            staff_id=staff_id,
        )
        handle_errors(response)
        response_data = response.json()
        return [
            datetime.date.fromisoformat(date)
            for date in response_data['shift_dates']
        ]

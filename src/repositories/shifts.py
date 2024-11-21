import datetime
from collections.abc import Iterable

from pydantic import TypeAdapter

from connections import ShiftConnection
from models import (
    CarWash, Shift, ShiftCreateResult, ShiftFinishResult,
    ShiftListPage,
)
from repositories.errors import handle_errors

__all__ = ('ShiftRepository',)


class ShiftRepository:

    def __init__(self, connection: ShiftConnection):
        self.__connection = connection

    async def get_list(
            self,
            *,
            date_from: datetime.date | None = None,
            date_to: datetime.date | None = None,
            staff_ids: Iterable[int] | None = None,
            limit: int | None = None,
            offset: int | None = None,
    ) -> ShiftListPage:
        response = await self.__connection.get_list(
            date_from=date_from,
            date_to=date_to,
            staff_ids=staff_ids,
            limit=limit,
            offset=offset,
        )
        print(response.text)
        handle_errors(response)
        response_data = response.json()
        return ShiftListPage.model_validate(response_data)

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
            statement_photo_file_id: str,
            service_app_photo_file_id: str,
    ) -> ShiftFinishResult:
        """
        Finish current shift of staff.

        Keyword Args:
            staff_id: Staff Telegram ID.
            statement_photo_file_id: File ID of photo of statement.
            service_app_photo_file_id: File ID of photo of service application.

        Returns:
            Response from the API.
        """
        response = await self.__connection.finish(
            staff_id=staff_id,
            statement_photo_file_id=statement_photo_file_id,
            service_app_photo_file_id=service_app_photo_file_id,
        )
        handle_errors(response)
        response_data = response.json()
        return ShiftFinishResult.model_validate(response_data)

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
            immediate_start: bool = False,
            car_wash_id: int | None = None,
            is_extra: bool = False,
    ) -> ShiftCreateResult:
        response = await self.__connection.create(
            staff_id=staff_id,
            dates=dates,
            immediate_start=immediate_start,
            car_wash_id=car_wash_id,
            is_extra=is_extra,
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

import datetime
from collections.abc import Iterable

from pydantic import TypeAdapter

from connections import ShiftConnection
from models import (
    CarWash, Shift, ShiftExtraCreateResult, ShiftFinishResult, ShiftListPage,
    ShiftRegularCreateResult, ShiftTestCreateResult, ShiftWithCarWashAndStaff,
)
from repositories.errors import handle_errors

__all__ = ('ShiftRepository',)


class ShiftRepository:

    def __init__(self, connection: ShiftConnection):
        self.__connection = connection

    async def get_by_id(self, shift_id: int) -> ShiftWithCarWashAndStaff:
        response = await self.__connection.get_by_id(shift_id)
        handle_errors(response)
        return ShiftWithCarWashAndStaff.model_validate_json(response.text)

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
            photo_file_ids: Iterable[str],
    ) -> ShiftFinishResult:
        """
        Finish current shift of staff.

        Keyword Args:
            staff_id: Staff Telegram ID.
            photo_file_ids: File ID of photo of statement or service app.

        Returns:
            Response from the API.
        """
        response = await self.__connection.finish(
            staff_id=staff_id,
            photo_file_ids=photo_file_ids,
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

    async def create_regular(
            self,
            *,
            staff_id: int,
            dates: list[datetime.date],
    ) -> ShiftRegularCreateResult:
        response = await self.__connection.create_regular(
            staff_id=staff_id,
            dates=dates,
        )
        handle_errors(response)
        response_data = response.json()
        return ShiftRegularCreateResult.model_validate(response_data)

    async def create_extra(
            self,
            *,
            staff_id: int,
            shift_date: datetime.date,
    ) -> ShiftExtraCreateResult:
        response = await self.__connection.create_extra(
            staff_id=staff_id,
            shift_date=shift_date,
        )
        handle_errors(response)
        response_data = response.json()
        return ShiftExtraCreateResult.model_validate(response_data)

    async def create_test(
            self,
            *,
            staff_id: int,
            shift_date: datetime.date,
    ) -> ShiftTestCreateResult:
        response = await self.__connection.create_test(
            staff_id=staff_id,
            shift_date=shift_date,
        )
        handle_errors(response)
        response_data = response.json()
        return ShiftTestCreateResult.model_validate(response_data)

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

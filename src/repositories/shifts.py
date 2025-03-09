import datetime
from collections.abc import Iterable

from pydantic import TypeAdapter

from connections import ShiftConnection
from models import (
    CarWash, Shift, ShiftExtraCreateResult, ShiftFinishResult, ShiftListPage,
    ShiftRegularCreateResult, ShiftTestCreateResult, ShiftWithCarWashAndStaff,
    DeadSoulsForMonth, StaffIdAndDate, StaffShiftMonths,
    TransferredCarsListResponse,
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
            from_date: datetime.date | None = None,
            to_date: datetime.date | None = None,
            staff_ids: Iterable[int] | None = None,
            limit: int | None = None,
            offset: int | None = None,
            shift_types: Iterable[str] | None = None,
    ) -> ShiftListPage:
        response = await self.__connection.get_list(
            from_date=from_date,
            to_date=to_date,
            staff_ids=staff_ids,
            limit=limit,
            offset=offset,
            shift_types=shift_types,
        )
        handle_errors(response)
        response_data = response.json()
        return ShiftListPage.model_validate(response_data)

    async def get_active(self, staff_id: int) -> int:
        response = await self.__connection.get_active(staff_id)
        handle_errors(response)
        return response.json()['id']

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
    ) -> None:
        response = await self.__connection.start(
            shift_id=shift_id,
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
            shifts: Iterable[StaffIdAndDate],
    ) -> ShiftExtraCreateResult:
        response = await self.__connection.create_extra(shifts)
        handle_errors(response)
        return ShiftExtraCreateResult.model_validate_json(response.text)

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

    async def get_months(self, staff_id: int) -> StaffShiftMonths:
        response = await self.__connection.get_months(staff_id=staff_id)
        handle_errors(response)
        return StaffShiftMonths.model_validate_json(response.text)

    async def reject(self, shift_id: int) -> None:
        response = await self.__connection.reject(shift_id=shift_id)
        handle_errors(response)

    async def get_dead_souls(
            self,
            *,
            month: int,
            year: int,
    ) -> DeadSoulsForMonth:
        response = await self.__connection.get_dead_souls(
            month=month,
            year=year,
        )
        handle_errors(response)
        return DeadSoulsForMonth.model_validate_json(response.text)

    async def confirm(self, *, shift_id: int) -> None:
        response = await self.__connection.confirm(shift_id=shift_id)
        handle_errors(response)

    async def get_transferred_cars(
            self,
            *,
            shift_id: int,
    ) -> TransferredCarsListResponse:
        response = await self.__connection.get_transferred_cars(
            shift_id=shift_id,
        )
        handle_errors(response)
        return TransferredCarsListResponse.model_validate_json(response.text)

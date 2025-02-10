import datetime

from pydantic import TypeAdapter

from connections import CarToWashConnection
from models import (
    CarToWashWebAppData, Car, CarAdditionalServices, CarToWashCreateResult,
    ShiftCarsCountByStaff,
    ShiftCarsWithoutWindshieldWasher,
)
from repositories.errors import handle_errors

__all__ = ('CarToWashRepository',)


class CarToWashRepository:

    def __init__(self, connection: CarToWashConnection):
        self.__connection = connection

    async def create(
            self,
            *,
            staff_id: int,
            car_to_wash: CarToWashWebAppData,
    ) -> CarToWashCreateResult:
        response = await self.__connection.create(
            staff_id=staff_id,
            car_to_wash=car_to_wash,
        )
        handle_errors(response)
        response_data = response.json()
        return CarToWashCreateResult.model_validate(response_data)

    async def get_all(self, staff_id: int) -> list[Car]:
        response = await self.__connection.get_all(staff_id)
        handle_errors(response)
        response_data = response.json()
        type_adapter = TypeAdapter(list[Car])
        return type_adapter.validate_python(response_data['cars'])

    async def update_additional_services(
            self,
            car_additional_services: CarAdditionalServices,
    ) -> None:
        data = car_additional_services.model_dump()
        response = await self.__connection.update_additional_services(
            car_id=car_additional_services.id,
            additional_services=data['additional_services'],
            windshield_washer_refilled_bottle_percentage=(
                data['windshield_washer_refilled_bottle_percentage']
            ),
        )
        handle_errors(response)

    async def get_count_by_staff(
            self,
            date: datetime.date,
    ) -> ShiftCarsCountByStaff:
        """Get count of cars by staff.

        Args:
            date: Date that shift scheduled on.

        Returns:
            ShiftCarsCountByStaff: Count of cars by staff.
        """
        response = await self.__connection.get_count_by_staff(date)
        handle_errors(response)
        response_data = response.json()
        return ShiftCarsCountByStaff.model_validate(response_data)

    async def get_without_windshield_washer(
            self,
            date: datetime.date,
    ) -> ShiftCarsWithoutWindshieldWasher:
        response = await self.__connection.get_without_windshield_washer(date)
        handle_errors(response)
        response_data = response.json()
        return ShiftCarsWithoutWindshieldWasher.model_validate(response_data)

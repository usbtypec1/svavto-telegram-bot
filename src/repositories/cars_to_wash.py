import datetime

from pydantic import TypeAdapter

from connections import CarToWashConnection
from models import CarToWash, Car, CarAdditionalServices, ShiftCarsCountByStaff, \
    ShiftCarsWithoutWindshieldWasher
from repositories.errors import handle_errors

__all__ = ('CarToWashRepository',)


class CarToWashRepository:

    def __init__(self, connection: CarToWashConnection):
        self.__connection = connection

    async def create(self, car_to_wash: CarToWash):
        response = await self.__connection.create(car_to_wash)

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
        response = await self.__connection.update_additional_services(
            car_id=car_additional_services.car_id,
            additional_services=car_additional_services.model_dump()[
                'additional_services'],
        )
        handle_errors(response)

    async def get_count_by_staff(
            self,
            date: datetime.date,
    ) -> ShiftCarsCountByStaff:
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

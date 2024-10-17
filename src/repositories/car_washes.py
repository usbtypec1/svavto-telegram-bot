from http.client import error

from pydantic import TypeAdapter

from connections import CarWashConnection
from logger import create_logger
from models import CarWash
from repositories.errors import handle_errors

__all__ = ('CarWashRepository',)

logger = create_logger('repositories')


class CarWashRepository:

    def __init__(self, connection: CarWashConnection):
        self.__connection = connection

    async def get_all(self) -> list[CarWash]:
        response = await self.__connection.get_all()
        handle_errors(response)
        response_data = response.json()
        type_adapter = TypeAdapter(list[CarWash])
        return type_adapter.validate_python(response_data['car_washes'])

    async def create(self, name: str) -> CarWash:
        response = await self.__connection.create(name)
        handle_errors(response)
        response_data = response.json()
        return CarWash.model_validate(response_data)

    async def get_by_id(self, car_wash_id: int) -> CarWash:
        response = await self.__connection.get_by_id(car_wash_id)
        handle_errors(response)
        response_data = response.json()
        return CarWash.model_validate(response_data)

    async def update(self, *, car_wash_id: int, name: str) -> None:
        response = await self.__connection.update(
            car_wash_id=car_wash_id,
            name=name,
        )
        handle_errors(response)

    async def delete_by_id(self, car_wash_id: int) -> None:
        response = await self.__connection.delete_by_id(car_wash_id)
        handle_errors(response)

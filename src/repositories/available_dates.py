from pydantic import TypeAdapter

from connections import AvailableDateConnection
from models import AvailableDate
from repositories.errors import handle_errors

__all__ = ('AvailableDateRepository',)


class AvailableDateRepository:

    def __init__(self, connection: AvailableDateConnection):
        self.__connection = connection

    async def get_all(self) -> list[AvailableDate]:
        response = await self.__connection.get_all()
        handle_errors(response)
        response_data = response.json()
        type_adapter = TypeAdapter(list[AvailableDate])
        return type_adapter.validate_python(response_data['available_dates'])

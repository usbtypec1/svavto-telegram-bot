from pydantic import TypeAdapter

from connections import CarWashConnection
from models import CarWash

__all__ = ('CarWashRepository',)

from repositories.errors import handle_errors


class CarWashRepository:

    def __init__(self, connection: CarWashConnection):
        self.__connection = connection

    async def get_all(self) -> list[CarWash]:
        type_adapter = TypeAdapter(list[CarWash])
        handle_errors()

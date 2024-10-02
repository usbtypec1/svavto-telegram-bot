from connections import PerformerConnection
from models import Performer
from repositories.errors import handle_errors

__all__ = ('PerformerRepository',)


class PerformerRepository:

    def __init__(self, connection: PerformerConnection):
        self.__connection = connection

    async def get_user_by_id(self, user_id: int) -> Performer:
        response = await self.__connection.get_by_id(user_id)
        response_data = response.json()
        handle_errors(response)
        return Performer.model_validate(response_data)

from connections import EconomicsConnection
from models import Penalty
from repositories.errors import handle_errors

__all__ = ('EconomicsRepository',)


class EconomicsRepository:

    def __init__(self, connection: EconomicsConnection):
        self.__connection = connection

    async def create_penalty(
            self,
            *,
            staff_id: int,
            reason: str,
    ) -> Penalty:
        response = await self.__connection.create_penalty(
            staff_id=staff_id,
            reason=reason,
        )
        handle_errors(response)
        response_data = response.json()
        return Penalty.model_validate(response_data)

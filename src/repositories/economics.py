from connections import EconomicsConnection
from models import Penalty, Surcharge
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
            amount: int | None,
    ) -> Penalty:
        response = await self.__connection.create_penalty(
            staff_id=staff_id,
            reason=reason,
            amount=amount,
        )
        handle_errors(response)
        response_data = response.json()
        return Penalty.model_validate(response_data)

    async def create_surcharge(
            self,
            *,
            staff_id: int,
            reason: str,
            amount: int,
    ) -> Surcharge:
        response = await self.__connection.create_surcharge(
            staff_id=staff_id,
            reason=reason,
            amount=amount,
        )
        handle_errors(response)
        response_data = response.json()
        return Surcharge.model_validate(response_data)

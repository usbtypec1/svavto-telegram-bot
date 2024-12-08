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
            shift_id: int,
            reason: str,
            amount: int | None,
    ) -> Penalty:
        """
        Give penalty to staff member.

        Keyword Args:
            staff_id: staff member ID
            shift_id: shift ID.
            reason: penalty reason.
            amount: optional penalty amount.

        Returns:
            Penalty: created penalty.
        """
        response = await self.__connection.create_penalty(
            staff_id=staff_id,
            shift_id=shift_id,
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
            shift_id: int,
            reason: str,
            amount: int,
    ) -> Surcharge:
        """
        Give surcharge to staff member.

        Keyword Args:
            staff_id: staff member ID
            shift_id: shift ID.
            reason: penalty reason.
            amount: optional penalty amount.

        Returns:
            Surcharge: created surcharge.
        """
        response = await self.__connection.create_surcharge(
            staff_id=staff_id,
            shift_id=shift_id,
            reason=reason,
            amount=amount,
        )
        handle_errors(response)
        response_data = response.json()
        return Surcharge.model_validate(response_data)

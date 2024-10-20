from connections import ShiftConnection
from repositories.errors import handle_errors


class ShiftRepository:

    def __init__(self, connection: ShiftConnection):
        self.__connection = connection

    async def get_active(self, staff_id: int):
        response = await self.__connection.get_active(staff_id)
        handle_errors(response)
        response_data: dict = response.json()

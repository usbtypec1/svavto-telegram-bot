from repositories import PerformerRepository

__all__ = ('UserService',)


class UserService:

    def __init__(self, user_repository: PerformerRepository):
        self.__user_repository = user_repository

    async def get_user_by_id(self, user_id: int):
        pass

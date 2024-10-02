from fast_depends import Depends

from connections import PerformerConnection
from dependencies.connections import get_performer_connection
from repositories.performers import PerformerRepository

__all__ = ('get_performer_repository',)


def get_performer_repository(
        connection: PerformerConnection = Depends(get_performer_connection),
) -> PerformerRepository:
    return PerformerRepository(connection)

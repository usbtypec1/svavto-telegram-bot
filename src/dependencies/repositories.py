from fast_depends import Depends

from connections import PerformerConnection, CarWashConnection
from dependencies.connections import (
    get_performer_connection,
    get_car_wash_connection,
)
from repositories import CarWashRepository
from repositories.performers import PerformerRepository

__all__ = ('get_performer_repository',)


def get_performer_repository(
        connection: PerformerConnection = Depends(get_performer_connection),
) -> PerformerRepository:
    return PerformerRepository(connection)


def get_car_wash_repository(
        connection: CarWashConnection = Depends(get_car_wash_connection),
) -> CarWashRepository:
    return CarWashRepository(connection)

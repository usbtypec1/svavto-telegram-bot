from fast_depends import Depends

from connections import StaffConnection, CarWashConnection, ShiftConnection
from dependencies.connections import (
    get_staff_connection,
    get_car_wash_connection,
    get_shift_connection,
)
from repositories import CarWashRepository, ShiftRepository, StaffRepository

__all__ = ('get_staff_repository', 'get_car_wash_repository')


def get_staff_repository(
        connection: StaffConnection = Depends(get_staff_connection),
) -> StaffRepository:
    return StaffRepository(connection)


def get_car_wash_repository(
        connection: CarWashConnection = Depends(get_car_wash_connection),
) -> CarWashRepository:
    return CarWashRepository(connection)


def get_shift_repository(
        connection: ShiftConnection = Depends(get_shift_connection),
) -> ShiftRepository:
    return ShiftRepository(connection)

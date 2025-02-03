from typing import Annotated

from fast_depends import Depends

from connections import (
    StaffConnection,
    CarWashConnection,
    ShiftConnection,
    EconomicsConnection,
    CarToWashConnection,
    AvailableDateConnection,
)
from dependencies.connections import (
    get_staff_connection,
    get_car_wash_connection,
    get_shift_connection,
    get_economics_connection,
    get_car_to_wash_connection,
    get_available_date_connection,
)
from repositories import (
    CarWashRepository,
    ShiftRepository,
    StaffRepository,
    EconomicsRepository,
    CarToWashRepository,
    AvailableDateRepository,
)

__all__ = (
    'get_staff_repository',
    'get_car_wash_repository',
    'get_economics_repository',
    'get_shift_repository',
    'get_car_to_wash_repository',
    'get_available_date_repository',
    'ShiftRepositoryDependency',
    'CarWashRepositoryDependency',
)


def get_available_date_repository(
        connection: AvailableDateConnection = Depends(
            get_available_date_connection,
        ),
) -> AvailableDateRepository:
    return AvailableDateRepository(connection)


def get_car_to_wash_repository(
        connection: CarToWashConnection = Depends(get_car_to_wash_connection),
) -> CarToWashRepository:
    return CarToWashRepository(connection)


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


def get_economics_repository(
        connection: EconomicsConnection = Depends(get_economics_connection),
) -> EconomicsRepository:
    return EconomicsRepository(connection)


ShiftRepositoryDependency = Annotated[
    ShiftRepository,
    Depends(get_shift_repository),
]

CarWashRepositoryDependency = Annotated[
    CarWashRepository,
    Depends(get_car_wash_repository),
]



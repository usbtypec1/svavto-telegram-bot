from fast_depends import Depends

from connections import (
    StaffConnection,
    CarWashConnection,
    ShiftConnection,
    EconomicsConnection,
    MailingConnection, CarToWashConnection,
)
from dependencies.connections import (
    get_staff_connection,
    get_car_wash_connection,
    get_shift_connection,
    get_economics_connection,
    get_mailing_connection, get_car_to_wash_connection,
)
from repositories import (
    CarWashRepository,
    ShiftRepository,
    StaffRepository,
    EconomicsRepository,
    MailingRepository,
    CarToWashRepository,
)

__all__ = (
    'get_staff_repository',
    'get_car_wash_repository',
    'get_economics_repository',
    'get_shift_repository',
    'get_mailing_repository',
    'get_car_to_wash_repository',
)


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


def get_mailing_repository(
        connection: MailingConnection = Depends(get_mailing_connection),
) -> MailingRepository:
    return MailingRepository(connection)

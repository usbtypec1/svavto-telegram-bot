import httpx
from fast_depends import Depends

from connections import (
    StaffConnection,
    CarWashConnection,
    ShiftConnection,
    EconomicsConnection,
    MailingConnection,
    CarToWashConnection,
)
from dependencies.http_clients import get_http_client

__all__ = (
    'get_staff_connection',
    'get_car_wash_connection',
    'get_shift_connection',
    'get_economics_connection',
    'get_mailing_connection',
    'get_car_to_wash_connection',
)


def get_car_to_wash_connection(
        http_client: httpx.AsyncClient = Depends(
            dependency=get_http_client,
            use_cache=False,
        ),
) -> CarToWashConnection:
    return CarToWashConnection(http_client)


def get_staff_connection(
        http_client: httpx.AsyncClient = Depends(
            dependency=get_http_client,
            use_cache=False,
        ),
) -> StaffConnection:
    return StaffConnection(http_client)


def get_car_wash_connection(
        http_client: httpx.AsyncClient = Depends(
            dependency=get_http_client,
            use_cache=False,
        ),
) -> CarWashConnection:
    return CarWashConnection(http_client)


def get_shift_connection(
        http_client: httpx.AsyncClient = Depends(
            dependency=get_http_client,
            use_cache=False,
        ),
) -> ShiftConnection:
    return ShiftConnection(http_client)


def get_economics_connection(
        http_client: httpx.AsyncClient = Depends(
            dependency=get_http_client,
            use_cache=False,
        ),
) -> EconomicsConnection:
    return EconomicsConnection(http_client)


def get_mailing_connection(
        http_client: httpx.AsyncClient = Depends(
            dependency=get_http_client,
            use_cache=False,
        ),
) -> MailingConnection:
    return MailingConnection(http_client)

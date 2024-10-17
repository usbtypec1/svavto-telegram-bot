import httpx
from fast_depends import Depends

from connections import PerformerConnection, CarWashConnection
from dependencies.http_clients import get_http_client

__all__ = (
    'get_performer_connection',
    'get_car_wash_connection',
)


def get_performer_connection(
        http_client: httpx.AsyncClient = Depends(
            dependency=get_http_client,
            use_cache=False,
        ),
) -> PerformerConnection:
    return PerformerConnection(http_client)


def get_car_wash_connection(
        http_client: httpx.AsyncClient = Depends(
            dependency=get_http_client,
            use_cache=False,
        ),
) -> CarWashConnection:
    return CarWashConnection(http_client)

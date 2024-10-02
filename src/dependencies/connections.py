import httpx
from fast_depends import Depends

from connections import PerformerConnection
from dependencies.http_clients import get_http_client

__all__ = ('get_performer_connection',)


def get_performer_connection(
        http_client: httpx.AsyncClient = Depends(
            dependency=get_http_client,
            use_cache=False,
        ),
) -> PerformerConnection:
    return PerformerConnection(http_client)

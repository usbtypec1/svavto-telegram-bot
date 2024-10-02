import httpx

__all__ = ('ApiConnection',)


class ApiConnection:

    def __init__(self, http_client: httpx.AsyncClient):
        self._http_client = http_client

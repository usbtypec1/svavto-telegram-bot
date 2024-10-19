from collections.abc import Iterable
from typing import Never

import httpx

from enums import ServerApiErrorCode
from exceptions import StaffNotFoundError, ServerApiError, \
    StaffAlreadyExistsError

__all__ = (
    'handle_errors',
    'raise_appropriate_error',
    'code_to_exception_class',
)

code_to_exception_class: dict[ServerApiErrorCode, type[Exception]] = {
    ServerApiErrorCode.STAFF_NOT_FOUND: StaffNotFoundError,
    ServerApiErrorCode.STAFF_ALREADY_EXISTS: StaffAlreadyExistsError,
}


def raise_appropriate_error(errors: Iterable[dict]) -> Never:
    for error in errors:
        error_code = error['code']
        error_detail = error['detail']

        exception_class = code_to_exception_class.get(error_code)
        if exception_class is not None:
            raise exception_class(error_detail)

    raise ServerApiError


def handle_errors(response: httpx.Response) -> Never | None:
    if response.is_error:
        response_data = response.json()
        raise_appropriate_error(response_data['errors'])

from collections.abc import Iterable
from typing import Never

import httpx

from enums import ServerApiErrorCode
from exceptions import (
    ShiftAlreadyConfirmedError, ShiftAlreadyFinishedError,
    ShiftByDateNotFoundError, ShiftNotConfirmedError,
    StaffHasActiveShiftError,
    StaffNotFoundError,
    ServerApiError,
    StaffAlreadyExistsError, StaffHasNoActiveShiftError, CarWashNotFoundError,
    CarWashSameAsCurrentError,
)

__all__ = (
    'handle_errors',
    'raise_appropriate_error',
    'code_to_exception_class',
)

code_to_exception_class: dict[ServerApiErrorCode, type[Exception]] = {
    ServerApiErrorCode.STAFF_NOT_FOUND: StaffNotFoundError,
    ServerApiErrorCode.STAFF_ALREADY_EXISTS: StaffAlreadyExistsError,
    ServerApiErrorCode.STAFF_HAS_NO_ACTIVE_SHIFT: StaffHasNoActiveShiftError,
    ServerApiErrorCode.CAR_WASH_NOT_FOUND: CarWashNotFoundError,
    ServerApiErrorCode.CAR_WASH_SAME_AS_CURRENT: CarWashSameAsCurrentError,
    ServerApiErrorCode.SHIFT_BY_DATE_NOT_FOUND: ShiftByDateNotFoundError,
    ServerApiErrorCode.SHIFT_NOT_CONFIRMED: ShiftNotConfirmedError,
    ServerApiErrorCode.STAFF_HAS_ACTIVE_SHIFT: StaffHasActiveShiftError,
    ServerApiErrorCode.SHIFT_ALREADY_FINISHED: ShiftAlreadyFinishedError,
    ServerApiErrorCode.SHIFT_ALREADY_CONFIRMED: ShiftAlreadyConfirmedError,
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

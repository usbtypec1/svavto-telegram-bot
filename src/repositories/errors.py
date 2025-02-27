from collections.abc import Iterable
from typing import Never

import httpx

from enums import ServerApiErrorCode
from exceptions import (
    AdditionalServicesCouldNotBeProvidedError, CarAlreadyWashedOnShiftError,
    CarWashNotFoundError,
    CarWashSameAsCurrentError, InvalidTimeToStartShiftError, ServerApiError,
    ShiftAlreadyConfirmedError,
    ShiftAlreadyExistsError, ShiftAlreadyFinishedError,
    ShiftNotConfirmedError,
    ShiftNotFoundError, StaffAlreadyExistsError, StaffHasActiveShiftError,
    StaffHasNoActiveShiftError, StaffNotFoundError,
    StaffRegisterRequestAlreadyExistsError,
)
from logger import create_logger


__all__ = (
    'handle_errors',
    'raise_appropriate_error',
    'code_to_exception_class',
)

logger = create_logger('errors')

code_to_exception_class: dict[ServerApiErrorCode, type[Exception]] = {
    ServerApiErrorCode.STAFF_NOT_FOUND: StaffNotFoundError,
    ServerApiErrorCode.STAFF_ALREADY_EXISTS: StaffAlreadyExistsError,
    ServerApiErrorCode.STAFF_HAS_NO_ACTIVE_SHIFT: StaffHasNoActiveShiftError,
    ServerApiErrorCode.CAR_WASH_NOT_FOUND: CarWashNotFoundError,
    ServerApiErrorCode.CAR_WASH_SAME_AS_CURRENT: CarWashSameAsCurrentError,
    ServerApiErrorCode.SHIFT_NOT_CONFIRMED: ShiftNotConfirmedError,
    ServerApiErrorCode.STAFF_HAS_ACTIVE_SHIFT: StaffHasActiveShiftError,
    ServerApiErrorCode.SHIFT_ALREADY_FINISHED: ShiftAlreadyFinishedError,
    ServerApiErrorCode.SHIFT_ALREADY_CONFIRMED: ShiftAlreadyConfirmedError,
    ServerApiErrorCode.SHIFT_NOT_FOUND: ShiftNotFoundError,
    ServerApiErrorCode.CAR_ALREADY_WASHED_ON_SHIFT: (
        CarAlreadyWashedOnShiftError
    ),
    ServerApiErrorCode.SHIFT_ALREADY_EXISTS: ShiftAlreadyExistsError,
    ServerApiErrorCode.ADDITIONAL_SERVICE_COULD_NOT_BE_PROVIDED: (
        AdditionalServicesCouldNotBeProvidedError
    ),
    ServerApiErrorCode.STAFF_REGISTER_REQUEST_ALREADY_EXISTS: (
        StaffRegisterRequestAlreadyExistsError
    ),
    ServerApiErrorCode.INVALID_TIME_TO_START_SHIFT: (
        InvalidTimeToStartShiftError
    ),
}


def raise_appropriate_error(errors: Iterable[dict]) -> Never:
    for error in errors:
        error_code = error['code']
        error_detail = error['detail']
        error_extra = error.get('extra', {})

        exception_class = code_to_exception_class.get(error_code)
        if exception_class is not None:
            raise exception_class(error_detail, **error_extra)

    logger.error('Unknown API error. Errors: %s', errors)
    raise ServerApiError


def handle_errors(response: httpx.Response) -> Never | None:
    if response.is_error:
        response_data = response.json()
        raise_appropriate_error(response_data['errors'])

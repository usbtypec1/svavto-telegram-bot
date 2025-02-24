import datetime
from zoneinfo import ZoneInfo

from exceptions import (
    InvalidNumberError, ShiftDateExpiredError,
    ShiftDateHasNotComeError,
)
from services.shifts import get_current_shift_date

__all__ = ('parse_integer_number', 'validate_shift_date')



def parse_integer_number(number: str) -> int:
    try:
        return int(number)
    except ValueError:
        raise InvalidNumberError(number=number)


def validate_shift_date(
        *,
        shift_date: datetime.date | str,
        timezone: ZoneInfo,
) -> None:
    if isinstance(shift_date, str):
        shift_date = datetime.date.fromisoformat(shift_date)

    now_date = get_current_shift_date(timezone)

    if now_date > shift_date:
        raise ShiftDateExpiredError(shift_date=shift_date)
    elif now_date < shift_date:
        raise ShiftDateHasNotComeError(shift_date=shift_date)

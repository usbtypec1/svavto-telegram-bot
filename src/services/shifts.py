import datetime
from typing import Final, Protocol
from zoneinfo import ZoneInfo


__all__ = (
    'get_current_shift_date',
)


class HasIdAndDate(Protocol):
    id: int
    date: datetime.date


SHIFT_END_HOUR: Final[int] = 20


def get_current_shift_date(timezone: ZoneInfo) -> datetime.date:
    """
    The **shift date** is the date when the shift was scheduled to start.
    Since the shift begins at 10 PM and ends at 7 AM,
    it technically spans two calendar days.
    However, the shift date is considered to be the date of its starting
    moment.

    Args:
        timezone: Timezone of place the car wash is located in.

    Returns:
        The date of the shift.
    """
    now = datetime.datetime.now(timezone)
    if now.hour < SHIFT_END_HOUR:
        previous_day = now - datetime.timedelta(days=1)
        return previous_day.date()
    return now.date()

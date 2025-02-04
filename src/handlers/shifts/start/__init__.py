from aiogram import Router

from . import (
    errors, extra_shift, test_shift,
    today_shift, specific_dates, expired_shifts,
)

__all__ = ('router',)

router = Router(name=__name__)
router.include_routers(
    errors.router,
    today_shift.router,
    test_shift.router,
    specific_dates.router,
    extra_shift.router,
    expired_shifts.router,
)

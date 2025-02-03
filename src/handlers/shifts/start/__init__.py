from aiogram import Router

from . import (
    errors, extra_shift, test_shift,
    today_shift, specific_dates,
)

__all__ = ('router',)

router = Router(name=__name__)
router.include_routers(
    errors.router,
    today_shift.router,
    request.router,
    test_shift.router,
    extra_shift.router,
)

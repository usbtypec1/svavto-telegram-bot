from aiogram import Router

from . import amount, confirm, photo, reason, staff, shift, menu

__all__ = ('router',)

router = Router(name=__name__)
router.include_routers(
    photo.router,
    amount.router,
    staff.router,
    reason.router,
    confirm.router,
    shift.router,
    menu.router,
)

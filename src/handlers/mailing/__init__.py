from aiogram import Router

from . import all_staff, last_active, menu, specific_staff

__all__ = ('router',)

router = Router(name=__name__)
router.include_routers(
    all_staff.router,
    last_active.router,
    menu.router,
    specific_staff.router,
)

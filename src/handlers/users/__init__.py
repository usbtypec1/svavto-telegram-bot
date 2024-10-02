from aiogram import Router

from . import menu, register

__all__ = ('router',)

router = Router(name=__name__)
router.include_routers(
    menu.router,
    register.router,
)

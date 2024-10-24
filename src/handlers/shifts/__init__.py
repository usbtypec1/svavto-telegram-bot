from aiogram import Router

from . import start, add_car, menu

__all__ = ('router',)

router = Router(name=__name__)
router.include_router(start.router)
router.include_router(add_car.router)
router.include_router(menu.router)

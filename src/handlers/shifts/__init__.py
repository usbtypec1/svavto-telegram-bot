from aiogram import Router

from . import start, add_car, menu, cars_to_wash, errors, statistics

__all__ = ('router',)

router = Router(name=__name__)
router.include_router(start.router)
router.include_router(add_car.router)
router.include_router(menu.router)
router.include_router(cars_to_wash.router)
router.include_router(errors.router)
router.include_router(statistics.router)

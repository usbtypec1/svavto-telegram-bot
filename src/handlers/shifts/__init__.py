from aiogram import Router

from . import (
    start,
    add_car,
    menu,
    cars_to_wash,
    errors,
    statistics,
    change_car_wash,
    finish,
    apply,
)

__all__ = ('router',)

router = Router(name=__name__)
router.include_routers(
    apply.router,
    start.router,
    add_car.router,
    menu.router,
    cars_to_wash.router,
    errors.router,
    statistics.router,
    change_car_wash.router,
    finish.router,
)

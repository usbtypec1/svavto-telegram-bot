from aiogram import Router

from . import (
    start,
    menu,
    cars_to_wash,
    errors,
    change_car_wash,
    finish,
    apply,
    schedule_self,
    confirm,
    reject,
)

__all__ = ('router',)

router = Router(name=__name__)
router.include_routers(
    apply.router,
    start.router,
    menu.router,
    cars_to_wash.router,
    errors.router,
    change_car_wash.router,
    finish.router,
    schedule_self.router,
    confirm.router,
    reject.router,
)

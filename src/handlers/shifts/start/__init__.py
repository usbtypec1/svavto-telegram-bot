from aiogram import Router

from . import car_wash_choose, request, today, immediate

__all__ = ('router',)

router = Router(name=__name__)
router.include_routers(
    car_wash_choose.router,
    request.router,
    today.router,
    immediate.router,
)

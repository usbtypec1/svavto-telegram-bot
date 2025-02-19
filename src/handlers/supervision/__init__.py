from aiogram import Router

from . import dead_souls, car_transfers, menu, shift_confirmations

__all__ = ('router',)

router = Router(name=__name__)
router.include_routers(
    menu.router,
    dead_souls.router,
    car_transfers.router,
    shift_confirmations.router,
)

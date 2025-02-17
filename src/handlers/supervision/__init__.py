from aiogram import Router

from . import staff_without_shifts, car_transfers, menu, shift_confirmations

__all__ = ('router',)

router = Router(name=__name__)
router.include_routers(
    menu.router,
    staff_without_shifts.router,
    car_transfers.router,
    shift_confirmations.router,
)

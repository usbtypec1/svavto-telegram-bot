from aiogram import Router

from . import numbers

__all__ = ('router',)


router = Router(name=__name__)
router.include_router(numbers.router)
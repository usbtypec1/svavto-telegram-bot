from aiogram import Router

from . import name

__all__ = ('router',)

router = Router(name=__name__)
router.include_router(name.router)

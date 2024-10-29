from aiogram import Router

from . import list

__all__ = ('router',)

router = Router(name=__name__)
router.include_router(list.router)

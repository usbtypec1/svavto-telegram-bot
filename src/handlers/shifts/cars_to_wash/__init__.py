from aiogram import Router

from . import list, create

__all__ = ('router',)

router = Router(name=__name__)
router.include_routers(
    list.router,
    create.router,
)

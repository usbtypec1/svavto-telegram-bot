from aiogram import Router

from . import detail, list, update

__all__ = ('router',)

router = Router(name=__name__)
router.include_routers(
    detail.router,
    list.router,
    update.router,
)

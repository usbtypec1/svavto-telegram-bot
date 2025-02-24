from aiogram import Router

from . import list, create, detail, update, delete, errors

__all__ = ('router',)

router = Router(name=__name__)
router.include_routers(
    list.router,
    create.router,
    detail.router,
    update.router,
    delete.router,
    errors.router,
)

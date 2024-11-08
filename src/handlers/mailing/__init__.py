from aiogram import Router

from . import menu, text, photos, reply_markup, reject, confirm

__all__ = ('router',)

router = Router(name=__name__)
router.include_routers(
    menu.router,
    text.router,
    photos.router,
    reply_markup.router,
    reject.router,
    confirm.router,
)

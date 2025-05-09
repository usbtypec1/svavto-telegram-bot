from aiogram import Router

from . import ban_or_unban, schedule, type

__all__ = ('router',)

router = Router(name=__name__)
router.include_router(ban_or_unban.router)
router.include_router(schedule.router)
router.include_router(type.router)

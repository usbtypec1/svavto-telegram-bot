from aiogram import Bot

from services.notifications import MailingService

__all__ = ('get_maling_service',)


def get_maling_service(bot: Bot) -> MailingService:
    return MailingService(bot)

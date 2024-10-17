from collections.abc import Iterable

from aiogram import Bot
from aiogram.exceptions import TelegramAPIError

from models import Performer
from repositories import StaffRepository

from views.register import StaffRegisterNotificationView

__all__ = ('UserService', 'NotificationService')


class UserService:

    def __init__(self, user_repository: StaffRepository):
        self.__user_repository = user_repository

    async def get_user_by_id(self, user_id: int):
        pass


class NotificationService:

    def __init__(self, bot: Bot):
        self.__bot = bot

    async def send_new_user_notification(
            self,
            *,
            admin_user_ids: Iterable[int],
            performer: Performer,
    ) -> None:
        view = StaffRegisterNotificationView(performer)
        text = view.get_text()
        reply_markup = view.get_reply_markup()
        for admin_user_id in admin_user_ids:
            try:
                await self.__bot.send_message(
                    chat_id=admin_user_id,
                    text=text,
                    reply_markup=reply_markup,
                )
            except TelegramAPIError as error:
                # TODO log error
                pass

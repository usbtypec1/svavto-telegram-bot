from collections.abc import Iterable

from aiogram import Bot
from aiogram.exceptions import TelegramAPIError

from models import StaffToRegister, Staff
from repositories import StaffRepository
from views.register import StaffRegisterNotificationView

__all__ = ('NotificationService',)


class NotificationService:

    def __init__(self, bot: Bot):
        self.__bot = bot

    async def send_new_user_notification(
            self,
            *,
            admin_user_ids: Iterable[int],
            staff: StaffToRegister,
            staff_id: int,
    ) -> None:
        view = StaffRegisterNotificationView(staff, staff_id)
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

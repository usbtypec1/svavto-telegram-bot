from collections.abc import Iterable

from aiogram import Bot
from aiogram.exceptions import TelegramAPIError

__all__ = (
    'NotificationService',
    'SpecificChatsNotificationService',
)

from aiogram.utils.media_group import MediaType

from views.base import TextView


class NotificationService:

    def __init__(self, bot: Bot):
        self._bot = bot


class SpecificChatsNotificationService(NotificationService):

    def __init__(self, bot: Bot, chat_ids: Iterable[int]):
        super().__init__(bot)
        self._chat_ids = chat_ids

    async def send_view(
            self,
            view: TextView,
    ) -> None:
        text = view.get_text()
        reply_markup = view.get_reply_markup()
        for chat_id in self._chat_ids:
            try:
                await self._bot.send_message(
                    chat_id=chat_id,
                    text=text,
                    reply_markup=reply_markup,
                )
            except TelegramAPIError:
                pass

    async def send_media_group(
            self,
            media: list[MediaType]
    ):
        for chat_id in self._chat_ids:
            try:
                await self._bot.send_media_group(
                    media=media,
                    chat_id=chat_id,
                )
            except TelegramAPIError:
                pass

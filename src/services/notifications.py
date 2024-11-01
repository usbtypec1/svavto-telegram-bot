from collections.abc import Iterable

from aiogram import Bot
from aiogram.exceptions import TelegramAPIError
from aiogram.types import InlineKeyboardMarkup, InputMedia

__all__ = (
    'NotificationService',
    'SpecificChatsNotificationService',
)

from aiogram.utils.media_group import MediaType


class NotificationService:

    def __init__(self, bot: Bot):
        self._bot = bot


class SpecificChatsNotificationService(NotificationService):

    def __init__(self, bot: Bot, chat_ids: Iterable[int]):
        super().__init__(bot)
        self._chat_ids = chat_ids

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

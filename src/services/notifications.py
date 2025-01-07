import asyncio
from collections.abc import Iterable

from aiogram import Bot
from aiogram.exceptions import TelegramAPIError
from aiogram.types import InlineKeyboardMarkup, InputMediaPhoto
from aiogram.utils.media_group import MediaGroupBuilder, MediaType

from ui.views import TextView

__all__ = (
    'NotificationService',
    'SpecificChatsNotificationService',
    'MailingService',
)


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


class MailingService(NotificationService):

    async def send_text(
            self,
            *,
            chat_ids: Iterable[int],
            text: str,
            reply_markup: InlineKeyboardMarkup | None,
    ):
        for chat_id in chat_ids:
            try:
                await self._bot.send_message(
                    chat_id=chat_id,
                    text=text,
                    reply_markup=reply_markup,
                )
            except TelegramAPIError:
                pass
            finally:
                await asyncio.sleep(0.1)

    async def send_single_photo(
            self,
            *,
            chat_ids: Iterable[int],
            text: str,
            reply_markup: InlineKeyboardMarkup | None,
            photo_file_id: str,
    ):
        for chat_id in chat_ids:
            try:
                await self._bot.send_photo(
                    chat_id=chat_id,
                    photo=photo_file_id,
                    caption=text,
                    reply_markup=reply_markup,
                )
            except TelegramAPIError:
                pass
            finally:
                await asyncio.sleep(0.1)

    async def send_media_group(
            self,
            *,
            chat_ids: Iterable[int],
            text: str | None,
            photo_file_ids: Iterable[str],
    ):
        builder = MediaGroupBuilder(
            caption=text,
            media=[
                InputMediaPhoto(media=photo_file_id)
                for photo_file_id in photo_file_ids
            ]
        )
        media_group = builder.build()
        for chat_id in chat_ids:
            try:
                await self._bot.send_media_group(
                    chat_id=chat_id,
                    media=media_group,
                )
            except TelegramAPIError:
                pass
            finally:
                await asyncio.sleep(0.1)

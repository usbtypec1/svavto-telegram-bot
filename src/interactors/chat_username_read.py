from dataclasses import dataclass

from aiogram import Bot
from aiogram.exceptions import TelegramAPIError


__all__ = ('ChatUsernameReadInteractor',)


@dataclass(frozen=True, slots=True, kw_only=True)
class ChatUsernameReadInteractor:
    bot: Bot
    chat_id: int

    async def execute(self) -> str | None:
        try:
            chat = await self.bot.get_chat(self.chat_id)
        except TelegramAPIError:
            return None
        return chat.username

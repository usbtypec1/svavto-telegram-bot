from typing import TypeAlias

from aiogram import Bot
from aiogram.exceptions import TelegramAPIError
from aiogram.types import (
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    ForceReply,
    ReplyKeyboardRemove,
    Message,
    CallbackQuery,
)

__all__ = (
    'ReplyMarkup',
    'TextView',
    'answer_view',
    'edit_message_by_view',
    'answer_or_edit_message_by_view',
    'send_view',
)

ReplyMarkup: TypeAlias = (
        InlineKeyboardMarkup
        | ReplyKeyboardMarkup
        | ForceReply
        | ReplyKeyboardRemove
)


class TextView:
    text: str | None = None
    reply_markup: ReplyMarkup | None = None

    def get_text(self) -> str | None:
        return self.text

    def get_reply_markup(self) -> ReplyMarkup | None:
        return self.reply_markup


async def answer_view(message: Message, view: TextView) -> Message:
    return await message.answer(
        text=view.get_text(),
        reply_markup=view.get_reply_markup(),
    )


async def edit_message_by_view(message: Message, view: TextView) -> Message:
    return await message.edit_text(
        text=view.get_text(),
        reply_markup=view.get_reply_markup(),
    )


async def answer_or_edit_message_by_view(
        message_or_callback_query: Message | CallbackQuery,
        view: TextView,
) -> Message:
    if isinstance(message_or_callback_query, Message):
        return await answer_view(message_or_callback_query, view)
    return await edit_message_by_view(message_or_callback_query.message, view)


async def send_view(
        bot: Bot,
        view: TextView,
        *chat_ids: int,
) -> None:
    text = view.get_text()
    reply_markup = view.get_reply_markup()
    for chat_id in chat_ids:
        try:
            await bot.send_message(chat_id, text, reply_markup=reply_markup)
        except TelegramAPIError:
            pass

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
    'answer_media_group_view',
)

from aiogram.utils.media_group import MediaGroupBuilder, MediaType

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


class MediaGroupView:
    medias: list[MediaType] | None = None
    caption: str | None = None
    reply_markup: ReplyMarkup | None = None

    def get_caption(self) -> str | None:
        return self.caption

    def get_medias(self) -> list[MediaType] | None:
        return self.medias

    def as_media_group(self) -> list[MediaType]:
        media_group_builder = MediaGroupBuilder(
            media=self.get_medias(),
            caption=self.get_caption(),
        )
        return media_group_builder.build()

    def get_reply_markup(self) -> ReplyMarkup | None:
        return self.reply_markup


async def answer_view(message: Message, view: TextView) -> Message:
    return await message.answer(
        text=view.get_text(),
        reply_markup=view.get_reply_markup(),
    )


async def answer_media_group_view(
        message: Message,
        view: MediaGroupView,
) -> list[Message]:
    return await message.answer_media_group(
        media=view.as_media_group(),
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

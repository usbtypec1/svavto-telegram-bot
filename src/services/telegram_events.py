import json

from aiogram.types import (
    ErrorEvent, InlineKeyboardButton,
    InlineKeyboardMarkup, Message, Update,
)
from pydantic import TypeAdapter

from models import Button

__all__ = (
    'answer_appropriate_event',
    'parse_web_app_data_buttons',
    'parse_chat_ids_json',
    'format_accept_text',
    'format_reject_text',
    'reply_markup_to_buttons',
    'get_user_id_from_update',
    'answer_to_update',
)


async def answer_appropriate_event(event: ErrorEvent, text: str) -> None:
    if event.update.message is not None:
        await event.update.message.answer(text)
    elif event.update.callback_query is not None:
        await event.update.callback_query.answer(text=text, show_alert=True)
    else:
        raise ValueError(f'Invalid event update type: {event.update}')


def parse_web_app_data_buttons(web_app_data: str) -> InlineKeyboardMarkup:
    type_adapter = TypeAdapter(list[InlineKeyboardButton])
    buttons = type_adapter.validate_json(web_app_data)
    return InlineKeyboardMarkup(
        inline_keyboard=[[button] for button in buttons],
    )


def reply_markup_to_buttons(
        reply_markup: InlineKeyboardMarkup,
) -> list[list[Button]]:
    buttons: list[list[Button]] = []
    for row in reply_markup.inline_keyboard:
        for button in row:
            buttons.append([button.model_dump()])
    return buttons


def parse_chat_ids_json(data: str) -> list[int]:
    return json.loads(data)


def format_accept_text(message: Message) -> str:
    return f'{message.text}\n\n<i>✅ Подтверждено</i>'


def format_reject_text(message: Message) -> str:
    return f'{message.text}\n\n<i>❌ Отменено</i>'


def get_user_id_from_update(update: Update) -> int:
    if update.message is not None:
        return update.message.from_user.id
    if update.callback_query is not None:
        return update.callback_query.from_user.id
    raise ValueError(f'Invalid update type: {update}')


async def answer_to_update(update: Update, text: str) -> None:
    if update.message is not None:
        await update.message.answer(text)
    elif update.callback_query is not None:
        await update.callback_query.answer(text=text, show_alert=True)
    else:
        raise ValueError(f'Invalid update type: {update}')

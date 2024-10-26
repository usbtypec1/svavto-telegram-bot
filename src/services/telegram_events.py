import json

from aiogram.types import ErrorEvent, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from models import Button

__all__ = (
    'answer_appropriate_event',
    'parse_web_app_data_buttons',
    'parse_chat_ids_json',
)


async def answer_appropriate_event(event: ErrorEvent, text: str) -> None:
    if event.update.message is not None:
        await event.update.message.answer(text)
    elif event.update.callback_query is not None:
        await event.update.callback_query.answer(text=text, show_alert=True)
    else:
        raise ValueError(f'Invalid event update type: {event.update}')


def parse_web_app_data_buttons(web_app_data: str) -> InlineKeyboardMarkup:
    web_app_data = json.loads(web_app_data)
    keyboard = InlineKeyboardBuilder()
    keyboard.max_width = 1
    for button in web_app_data['buttons']:
        keyboard.button(
            text=button['text'],
            url=button['url'],
        )
    return keyboard.as_markup()


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

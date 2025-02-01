from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton

import ui.texts

__all__ = (
    'create_accept_button',
    'create_confirm_button',
    'create_reject_button',
    'create_back_button',
)


def create_accept_button(
        callback_data: CallbackData | str,
) -> InlineKeyboardButton:
    if isinstance(callback_data, CallbackData):
        callback_data = callback_data.pack()
    return InlineKeyboardButton(
        text=ui.texts.ACCEPT,
        callback_data=callback_data,
    )


def create_confirm_button(
        callback_data: CallbackData | str,
) -> InlineKeyboardButton:
    if isinstance(callback_data, CallbackData):
        callback_data = callback_data.pack()
    return InlineKeyboardButton(
        text=ui.texts.CONFIRM,
        callback_data=callback_data,
    )


def create_reject_button(
        callback_data: CallbackData | str,
) -> InlineKeyboardButton:
    if isinstance(callback_data, CallbackData):
        callback_data = callback_data.pack()
    return InlineKeyboardButton(
        text=ui.texts.REJECT,
        callback_data=callback_data,
    )


def create_back_button(
        callback_data: CallbackData | str,
) -> InlineKeyboardButton:
    if isinstance(callback_data, CallbackData):
        callback_data = callback_data.pack()
    return InlineKeyboardButton(
        text=ui.texts.BACK,
        callback_data=callback_data,
    )

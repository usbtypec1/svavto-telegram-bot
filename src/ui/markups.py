from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup

import ui.buttons

__all__ = ('create_accept_reject_markup',)


def create_accept_reject_markup(
        accept_callback_data: CallbackData | str,
        reject_callback_data: CallbackData | str,
) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                ui.buttons.create_accept_button(accept_callback_data),
                ui.buttons.create_reject_button(reject_callback_data),
            ],
        ],
    )

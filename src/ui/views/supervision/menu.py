from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from ui.views import ButtonText, TextView


class SupervisionMenuView(TextView):
    text = '🔍 Меню контроля'
    reply_markup = ReplyKeyboardMarkup(
        is_persistent=True,
        resize_keyboard=True,
        keyboard=[
            [
                KeyboardButton(text=ButtonText.SUPERVISION_CAR_TRANSFERS),
                KeyboardButton(text=ButtonText.SUPERVISION_SHIFT_CONFIRMATIONS),
            ],
            [
                KeyboardButton(
                    text=ButtonText.SUPERVISION_STAFF_WITHOUT_SHIFTS,
                ),
            ],
            [
                KeyboardButton(text=ButtonText.MAIN_MENU)
            ],
        ],
    )

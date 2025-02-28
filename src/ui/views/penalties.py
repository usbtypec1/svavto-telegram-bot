from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, WebAppInfo

from ui.views import ButtonText
from ui.views.base import TextView


__all__ = ('PenaltyCreateMenuView',)


class PenaltyCreateMenuView(TextView):
    text = '🛑 Меню штрафов'

    def __init__(self, *, web_app_base_url: str):
        self.__web_app_base_url = web_app_base_url

    def get_reply_markup(self) -> ReplyKeyboardMarkup:
        car_transporter_penalties_web_app_url = (
            f'{self.__web_app_base_url}/penalties/car-transporters'
        )
        car_wash_penalties_web_app_url = (
            f'{self.__web_app_base_url}/penalties/car-wash'
        )
        return ReplyKeyboardMarkup(
            resize_keyboard=True,
            keyboard=[
                [
                    KeyboardButton(
                        text=ButtonText.PENALTY_CREATE_CAR_TRANSPORTER,
                        web_app=WebAppInfo(
                            url=car_transporter_penalties_web_app_url,
                        )
                    ),
                ],
                [
                    KeyboardButton(
                        text=ButtonText.PENALTY_CREATE_CAR_WASH,
                        web_app=WebAppInfo(
                            url=car_wash_penalties_web_app_url,
                        )
                    ),
                ],
                [
                    KeyboardButton(
                        text=ButtonText.MAIN_MENU,
                    ),
                ],
            ],
        )

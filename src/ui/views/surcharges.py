from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, WebAppInfo

from ui.views import ButtonText
from ui.views.base import TextView


__all__ = ('SurchargeCreateMenuView',)


class SurchargeCreateMenuView(TextView):
    text = '💰 Меню доплат'

    def __init__(self, *, web_app_base_url: str):
        self.__web_app_base_url = web_app_base_url

    def get_reply_markup(self) -> ReplyKeyboardMarkup:
        transporter_surcharge_create_web_app_url = (
            f'{self.__web_app_base_url}/surcharges/car-transporter'
        )
        car_wash_surcharge_create_web_app_url = (
            f'{self.__web_app_base_url}/surcharges/car-wash'
        )
        return ReplyKeyboardMarkup(
            resize_keyboard=True,
            keyboard=[
                [
                    KeyboardButton(
                        text=ButtonText.SURCHARGE_CREATE_CAR_TRANSPORTER,
                        web_app=WebAppInfo(
                            url=transporter_surcharge_create_web_app_url,
                        ),
                    ),
                ],
                [
                    KeyboardButton(
                        text=ButtonText.SURCHARGE_CREATE_CAR_WASH,
                        web_app=WebAppInfo(
                            url=car_wash_surcharge_create_web_app_url,
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

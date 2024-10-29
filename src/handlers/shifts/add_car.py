from aiogram import Router, F
from aiogram.filters import StateFilter, invert_f
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, \
    WebAppInfo
from fast_depends import Depends, inject

from dependencies.repositories import get_car_to_wash_repository
from filters import admins_filter
from repositories import CarToWashRepository
from views.button_texts import ButtonText
from models import CarToWash

__all__ = ('router',)

router = Router(name=__name__)


@router.message(
    F.web_app_data.button_text == 'test-add-car',
    invert_f(admins_filter),
    StateFilter('*'),
)
@inject
async def on_input_car(
        message: Message,
        car_to_wash_repository: CarToWashRepository = Depends(
            dependency=get_car_to_wash_repository,
            use_cache=False,
        ),
) -> None:
    car_to_wash = CarToWash.model_validate(message.web_app_data.data)
    await car_to_wash_repository.create(car_to_wash)


@router.message(
    F.text == ButtonText.SHIFT_ADD_CAR,
    invert_f(admins_filter),
    StateFilter('*'),
)
async def on_start_shift_add_car_flow(
        message: Message,
) -> None:
    await message.reply(
        text='test',
        reply_markup=ReplyKeyboardMarkup(
            resize_keyboard=True,
            keyboard=[
                [
                    KeyboardButton(
                        text='test-add-car',
                        web_app=WebAppInfo(
                            url='https://avtomoykabot.store/app/shifts/add-car'
                        )
                    )
                ]
            ]
        )
    )

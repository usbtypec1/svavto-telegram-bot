from aiogram import F, Router
from aiogram.filters import StateFilter, invert_f
from aiogram.types import Message
from fast_depends import Depends, inject

from dependencies.repositories import get_car_to_wash_repository
from exceptions import CarAlreadyWashedOnShiftError
from filters import admins_filter
from models import CarToWashWebAppData
from repositories import CarToWashRepository
from views.button_texts import ButtonText

__all__ = ('router',)

router = Router(name=__name__)


@router.message(
    F.web_app_data.button_text == ButtonText.SHIFT_ADD_CAR,
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
    print(message.web_app_data.data)
    return
    car_to_wash_web_app_data = CarToWashWebAppData.model_validate_json(
        message.web_app_data.data,
    )
    try:
        car_to_wash = await car_to_wash_repository.create(
            staff_id=message.from_user.id,
            car_to_wash=car_to_wash_web_app_data,
        )
    except CarAlreadyWashedOnShiftError:
        await message.answer(
            f'❌ Авто с гос.номером {car_to_wash_web_app_data.number}'
            ' уже было добавлено',

        )
        return
    await message.answer(
        f'✅ Авто с гос.номером {car_to_wash.number} добавлено',
    )
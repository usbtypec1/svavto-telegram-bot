from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery, Message
from fast_depends import inject

from callback_data import (
    ShiftWorkTypeChoiceCallbackData,
)
from config import Config
from dependencies.repositories import (
    CarWashRepositoryDependency, ShiftRepositoryDependency,
)
from enums import ShiftWorkType
from exceptions import ShiftNotFoundError
from filters import staff_filter
from interactors import CarWashesReadInteractor, ShiftForTodayReadInteractor
from logger import create_logger
from ui.views import (
    answer_text_view, ButtonText, edit_message_by_view, ShiftCarWashUpdateView,
    ShiftWorkTypeChoiceView,
)


logger = create_logger(__name__)

router = Router(name=__name__)


@router.callback_query(
    ShiftWorkTypeChoiceCallbackData.filter(
        rule=F.work_type == ShiftWorkType.MOVE_TO_WASH,
    ),
    staff_filter,
    StateFilter('*'),
)
@inject
async def on_move_to_wash_shift_work_type_choice(
        callback_query: CallbackQuery,
        config: Config,
        shift_repository: ShiftRepositoryDependency,
        car_wash_repository: CarWashRepositoryDependency,
) -> None:
    interactor = ShiftForTodayReadInteractor(
        shift_repository=shift_repository,
        staff_id=callback_query.from_user.id,
        timezone=config.timezone,
    )
    try:
        shift = await interactor.execute()
    except ShiftNotFoundError:
        await callback_query.answer(
            text='❌У вас нет на сегодня смены',
            show_alert=True
        )
        return

    car_washes = await CarWashesReadInteractor(
        car_wash_repository=car_wash_repository
    ).execute()

    await shift_repository.start(shift_id=shift.id)

    view = ShiftCarWashUpdateView(car_washes)
    await edit_message_by_view(callback_query.message, view)


@router.callback_query(
    ShiftWorkTypeChoiceCallbackData.filter(),
    staff_filter,
    StateFilter('*'),
)
async def on_shift_work_type_choice(callback_query: CallbackQuery) -> None:
    await callback_query.answer('В разработке', show_alert=True)


@router.message(
    F.text == ButtonText.SHIFT_START,
    staff_filter,
    StateFilter('*'),
)
async def on_show_shift_work_types_list(
        message: Message,
) -> None:
    await answer_text_view(message, ShiftWorkTypeChoiceView())

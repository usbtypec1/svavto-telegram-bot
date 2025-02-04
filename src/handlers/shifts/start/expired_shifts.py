from aiogram import Router

from aiogram.filters import invert_f, StateFilter
from aiogram.types import CallbackQuery

from callback_data import ShiftStartCarWashCallbackData
from states import (
    ShiftTestStartStates, ShiftExtraStartStates,
    ShiftRegularStartStates, ShiftTodayStartStates,
)

__all__ = ('router',)

router = Router(name=__name__)


@router.callback_query(
    ShiftStartCarWashCallbackData.filter(),
    invert_f(
        StateFilter(
            ShiftTestStartStates.car_wash,
            ShiftExtraStartStates.car_wash,
            ShiftRegularStartStates.car_wash,
            ShiftTodayStartStates.car_wash,
        )
    ),
)
async def on_car_choose_on_expired_shift(
        callback_query: CallbackQuery,
) -> None:
    await callback_query.answer(
        text='❌ Невозможно начать смену, запрос устарел',
        show_alert=True,
    )
    await callback_query.message.delete()

import datetime

from aiogram import Bot, F, Router
from aiogram.filters import StateFilter, invert_f
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from fast_depends import Depends, inject

from callback_data import ShiftImmediateStartCallbackData
from config import Config
from dependencies.repositories import get_car_wash_repository
from filters import admins_filter
from models import DirectShiftWebAppData
from repositories import CarWashRepository
from services.notifications import SpecificChatsNotificationService
from states import ShiftStartStates
from ui.views import edit_message_by_view
from ui.views import ButtonText
from ui.views import (
    ShiftImmediateStartRequestView,
    ShiftStartCarWashChooseView,
)

__all__ = ('router',)

router = Router(name=__name__)


@router.callback_query(
    ShiftImmediateStartCallbackData.filter(),
    invert_f(admins_filter),
    StateFilter('*'),
)
@inject
async def on_immediate_start_shift(
        callback_query: CallbackQuery,
        callback_data: ShiftImmediateStartCallbackData,
        state: FSMContext,
        config: Config,
        car_wash_repository: CarWashRepository = Depends(
            dependency=get_car_wash_repository,
            use_cache=False,
        ),
) -> None:
    now_date = datetime.datetime.now(config.timezone).date()
    shift_date = datetime.date.fromisoformat(callback_data.date)
    if now_date > shift_date:
        await callback_query.answer(
            text='❌ Вы не можете начать запланированную в прошлом смену',
            show_alert=True,
        )
    elif now_date < shift_date:
        await callback_query.answer(
            text=(
                f'❌ Вы сможете начать только в {shift_date:%d.%m.%Y}'
            ),
            show_alert=True,
        )
    else:
        await state.set_state(ShiftStartStates.car_wash)
        await state.update_data(date=shift_date.isoformat())
        car_washes = await car_wash_repository.get_all()
        if not car_washes:
            await callback_query.answer(
                text='❌ Нет доступных моек',
                show_alert=True,
            )
            return
        view = ShiftStartCarWashChooseView(car_washes)
        await edit_message_by_view(callback_query.message, view)


@router.message(
    F.web_app_data.button_text == ButtonText.DIRECT_SHIFT,
    admins_filter,
    StateFilter('*'),
)
async def on_direct_shift_dates(
        message: Message,
        bot: Bot,
) -> None:
    direct_shift_web_app_data = DirectShiftWebAppData.model_validate_json(
        message.web_app_data.data
    )
    notification_service = SpecificChatsNotificationService(
        bot=bot,
        chat_ids=direct_shift_web_app_data.staff_ids,
    )
    view = ShiftImmediateStartRequestView(date=direct_shift_web_app_data.date)
    sent_message = await message.answer(
        text='🚀 Отправляются запросы на начало смены',
    )
    await notification_service.send_view(view=view)
    await sent_message.edit_text('✅ Запросы на начало смены отправлены')

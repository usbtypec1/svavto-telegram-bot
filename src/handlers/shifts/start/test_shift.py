import datetime

from aiogram import Bot, F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from fast_depends import inject

from callback_data import (
    ShiftStartCarWashCallbackData,
    TestShiftStartCallbackData,
)
from config import Config
from dependencies.repositories import (
    CarWashRepositoryDependency, ShiftRepositoryDependency,
)
from filters import admins_filter, staff_filter
from models import DirectShiftWebAppData
from services.notifications import SpecificChatsNotificationService
from services.validators import validate_shift_date
from states import ShiftTestStartStates
from ui.views import (
    ButtonText, ShiftMenuView, ShiftStartCarWashChooseView,
    TestShiftStartRequestView, answer_text_view, edit_message_by_view,
)

__all__ = ('router',)

router = Router(name=__name__)


@router.callback_query(
    ShiftStartCarWashCallbackData.filter(),
    staff_filter,
    StateFilter(ShiftTestStartStates.car_wash),
)
@inject
async def on_car_wash_choose(
        callback_query: CallbackQuery,
        callback_data: ShiftStartCarWashCallbackData,
        state: FSMContext,
        config: Config,
        shift_repository: ShiftRepositoryDependency,
) -> None:
    state_data: dict = await state.get_data()
    shift_id: int = state_data['shift_id']
    car_wash_id = callback_data.car_wash_id

    await shift_repository.start(
        shift_id=shift_id,
        car_wash_id=car_wash_id,
    )
    await callback_query.message.edit_text(
        text='✅ Вы начали тестовую смену водителя перегонщика на мойку',
    )
    view = ShiftMenuView(
        staff_id=callback_query.from_user.id,
        web_app_base_url=config.web_app_base_url,
    )
    await answer_text_view(callback_query.message, view)
    await callback_query.answer()


@router.callback_query(
    TestShiftStartCallbackData.filter(),
    staff_filter,
    StateFilter('*'),
)
@inject
async def on_extra_shift_start(
        callback_query: CallbackQuery,
        callback_data: TestShiftStartCallbackData,
        config: Config,
        state: FSMContext,
        shift_repository: ShiftRepositoryDependency,
        car_wash_repository: CarWashRepositoryDependency,
) -> None:
    shift_date = datetime.date.fromisoformat(callback_data.date)

    validate_shift_date(shift_date=callback_data.date, timezone=config.timezone)

    await state.set_state(ShiftTestStartStates.car_wash)
    await state.update_data(date=callback_data.date, is_extra=True)
    car_washes = await car_wash_repository.get_all()
    if not car_washes:
        await callback_query.answer(
            text='❌ Нет доступных моек',
            show_alert=True,
        )
        return

    shift_create_result = await shift_repository.create_test(
        staff_id=callback_query.from_user.id,
        shift_date=shift_date,
    )
    await state.update_data(shift_id=shift_create_result.shift_id)
    await state.set_state(ShiftTestStartStates.car_wash)
    view = ShiftStartCarWashChooseView(car_washes)
    await edit_message_by_view(callback_query.message, view)


@router.message(
    F.web_app_data.button_text == ButtonText.TEST_SHIFT_REQUEST,
    admins_filter,
    StateFilter('*'),
)
async def on_send_test_shift_start_requests(
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
    view = TestShiftStartRequestView(date=direct_shift_web_app_data.date)
    sent_message = await message.answer(
        text='🚀 Отправляются запросы на тестовый доступ',
    )
    await notification_service.send_view(view=view)
    await sent_message.edit_text('✅ Выданы тестовые доступы')

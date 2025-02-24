import datetime

from aiogram import Bot, F, Router
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery, Message
from fast_depends import inject

from callback_data import (
    TestShiftStartCallbackData,
)
from config import Config
from dependencies.repositories import (
    CarWashRepositoryDependency, ShiftRepositoryDependency,
)
from filters import admins_filter, staff_filter
from interactors import CarWashesReadInteractor
from logger import create_logger
from models import DirectShiftWebAppData
from services.notifications import SpecificChatsNotificationService
from services.validators import validate_shift_date
from ui.views import (
    ButtonText, edit_message_by_view, ShiftCarWashUpdateView,
    TestShiftStartRequestView,
)


__all__ = ('router',)

logger = create_logger('test_shifts')

router = Router(name=__name__)


@router.callback_query(
    TestShiftStartCallbackData.filter(),
    staff_filter,
    StateFilter('*'),
)
@inject
async def on_test_shift_start(
        callback_query: CallbackQuery,
        callback_data: TestShiftStartCallbackData,
        config: Config,
        shift_repository: ShiftRepositoryDependency,
        car_wash_repository: CarWashRepositoryDependency,
) -> None:
    shift_date = datetime.date.fromisoformat(callback_data.date)
    validate_shift_date(shift_date=shift_date, timezone=config.timezone)

    shift_create_result = await shift_repository.create_test(
        staff_id=callback_query.from_user.id,
        shift_date=shift_date,
    )
    await shift_repository.start(shift_id=shift_create_result.shift_id)

    car_washes = await CarWashesReadInteractor(car_wash_repository).execute()
    view = ShiftCarWashUpdateView(car_washes)
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

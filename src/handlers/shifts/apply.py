import datetime

from aiogram import Bot, F, Router
from aiogram.filters import StateFilter, invert_f
from aiogram.types import CallbackQuery, Message
from fast_depends import Depends, inject
from pydantic import TypeAdapter

from callback_data import ShiftApplyCallbackData
from config import Config
from dependencies.repositories import (
    get_available_date_repository,
    get_shift_repository,
)
from filters import admins_filter
from repositories import AvailableDateRepository, ShiftRepository
from services.notifications import SpecificChatsNotificationService
from views.base import answer_text_view
from views.button_texts import ButtonText
from views.menu import MainMenuView
from views.shifts import (
    ShiftApplyChooseMonthView,
    ShiftApplyScheduleMonthCalendarWebAppView,
    StaffShiftScheduleCreatedNotificationView,
)

__all__ = ('router',)

router = Router(name=__name__)


@router.message(
    F.web_app_data.button_text == ButtonText.SHIFT_SCHEDULE_MONTH_CALENDAR,
    invert_f(admins_filter),
    StateFilter('*'),
)
@inject
async def on_shift_schedule_month_calendar_input(
        message: Message,
        config: Config,
        admin_user_ids: set[int],
        bot: Bot,
        shift_repository: ShiftRepository = Depends(
            dependency=get_shift_repository,
            use_cache=False,
        ),
) -> None:
    admins_notification_service = SpecificChatsNotificationService(
        bot=bot,
        chat_ids=admin_user_ids,
    )
    type_adapter = TypeAdapter(list[datetime.date])
    shift_dates: list[datetime.date] = type_adapter.validate_json(
        message.web_app_data.data,
    )
    shift_create_result = await shift_repository.create(
        staff_id=message.from_user.id,
        dates=shift_dates,
    )
    await message.answer('✅ График успешно отправлен')
    view = MainMenuView(config.web_app_base_url)
    await answer_text_view(message, view)
    view = StaffShiftScheduleCreatedNotificationView(
        staff_full_name=shift_create_result.staff_full_name,
    )
    await admins_notification_service.send_view(view)


@router.callback_query(
    ShiftApplyCallbackData.filter(),
    invert_f(admins_filter),
    StateFilter('*'),
)
@inject
async def on_choose_month_apply_to_shift(
        callback_query: CallbackQuery,
        callback_data: ShiftApplyCallbackData,
        config: Config,
        shift_repository: ShiftRepository = Depends(
            dependency=get_shift_repository,
            use_cache=False,
        ),
) -> None:
    shifts = await shift_repository.get_shifts_by_staff_id(
        staff_id=callback_query.from_user.id,
        month=callback_data.month,
        year=callback_data.year,
    )
    not_test_shifts = [shift for shift in shifts if not shift.is_test]
    if not_test_shifts:
        await callback_query.answer(
            text=(
                'График за этот месяц уже заполнен.'
                ' Для внесения изменений обратитесь к старшему смены'
            ),
            show_alert=True,
        )
        return

    view = ShiftApplyScheduleMonthCalendarWebAppView(
        web_app_base_url=config.web_app_base_url,
        year=callback_data.year,
        month=callback_data.month,
    )
    await answer_text_view(callback_query.message, view)
    await callback_query.message.delete()


@router.message(
    F.text == ButtonText.SHIFT_APPLY,
    invert_f(admins_filter),
    StateFilter('*'),
)
@inject
async def on_shift_apply(
        message: Message,
        config: Config,
        available_dates: AvailableDateRepository = Depends(
            dependency=get_available_date_repository,
            use_cache=False,
        ),
) -> None:
    available_dates = await available_dates.get_all()
    view = ShiftApplyChooseMonthView(
        available_dates=available_dates,
        timezone=config.timezone,
    )
    await answer_text_view(message, view)

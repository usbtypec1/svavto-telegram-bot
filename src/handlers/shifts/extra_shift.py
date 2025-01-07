import datetime

from aiogram import Bot, F, Router
from aiogram.exceptions import TelegramAPIError
from aiogram.filters import StateFilter, invert_f
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from fast_depends import Depends, inject

from callback_data import (
    ExtraShiftCreateAcceptCallbackData,
    ExtraShiftCreateRejectCallbackData, ExtraShiftStartCallbackData,
)
from config import Config
from dependencies.repositories import (
    get_car_wash_repository,
    get_staff_repository,
)
from filters import admins_filter
from repositories import CarWashRepository, StaffRepository
from services.notifications import SpecificChatsNotificationService
from services.telegram_events import format_accept_text, format_reject_text
from states import ShiftStartStates
from ui.views import answer_text_view, send_text_view
from ui.views import ButtonText
from ui.views import MainMenuView
from ui.views import (
    ExtraShiftScheduleNotificationView,
    ExtraShiftScheduleWebAppView,
    ExtraShiftStartView,
    ShiftStartCarWashChooseView,
)

__all__ = ('router',)

router = Router(name=__name__)


@router.callback_query(
    ExtraShiftStartCallbackData.filter(),
    invert_f(admins_filter),
    StateFilter('*'),
)
@inject
async def on_extra_shift_start(
        callback_query: CallbackQuery,
        callback_data: ExtraShiftStartCallbackData,
        config: Config,
        state: FSMContext,
        car_wash_repository: CarWashRepository = Depends(
            dependency=get_car_wash_repository,
            use_cache=False,
        ),
) -> None:
    now_date = datetime.datetime.now(config.timezone).date()
    shift_date = datetime.date.fromisoformat(callback_data.date)
    if now_date > shift_date:
        await callback_query.answer(
            text='❌ Вы не можете начать запланированную в прошлом доп.смену',
            show_alert=True,
        )
    elif now_date < shift_date:
        await callback_query.answer(
            text=(
                f'❌ Вы сможете начать доп.смену только в {shift_date:%d.%m.%Y}'
            ),
            show_alert=True,
        )
    else:
        await state.set_state(ShiftStartStates.car_wash)
        await state.update_data(is_extra=True, date=shift_date.isoformat())
        car_washes = await car_wash_repository.get_all()
        if not car_washes:
            await callback_query.answer(
                text='❌ Нет доступных моек',
                show_alert=True,
            )
            return
        view = ShiftStartCarWashChooseView(car_washes)
        await answer_text_view(callback_query.message, view)


@router.callback_query(
    ExtraShiftCreateAcceptCallbackData.filter(),
    admins_filter,
    StateFilter('*'),
)
@inject
async def on_extra_shift_create_accept(
        callback_query: CallbackQuery,
        callback_data: ExtraShiftCreateAcceptCallbackData,
        bot: Bot,
        staff_repository: StaffRepository = Depends(
            dependency=get_staff_repository,
            use_cache=False,
        ),
) -> None:
    staff = await staff_repository.get_by_id(callback_data.staff_id)
    view = ExtraShiftStartView(
        staff_full_name=staff.full_name,
        shift_date=datetime.date.fromisoformat(callback_data.date),
    )
    sent_messages = await send_text_view(bot, view, callback_data.staff_id)
    if sent_messages[0] is None:
        await callback_query.answer(
            text='❌ Не удалось отправить сообщение сотруднику',
            show_alert=True,
        )
    else:
        await callback_query.message.edit_text(
            format_accept_text(callback_query.message),
        )


@router.callback_query(
    ExtraShiftCreateRejectCallbackData.filter(),
    admins_filter,
    StateFilter('*'),
)
async def on_extra_shift_create_reject(
        callback_query: CallbackQuery,
        callback_data: ExtraShiftCreateRejectCallbackData,
        bot: Bot,
) -> None:
    try:
        await bot.send_message(
            chat_id=callback_data.staff_id,
            text=(
                f'❌ Ваш запрос на доп.смену'
                f' {callback_data.date:%d.%m.%Y} отклонен'
            ),
        )
    except TelegramAPIError:
        await callback_query.answer(
            text='❌ Не удалось отправить сообщение сотруднику',
            show_alert=True,
        )
    else:
        await callback_query.message.edit_text(
            format_reject_text(callback_query.message),
        )


@router.message(
    F.web_app_data.button_text == ButtonText.EXTRA_SHIFT_CALENDAR,
    invert_f(admins_filter),
    StateFilter('*'),
)
@inject
async def on_extra_shift_calendar(
        message: Message,
        config: Config,
        admin_user_ids: set[int],
        bot: Bot,
        staff_repository: StaffRepository = Depends(
            dependency=get_staff_repository,
            use_cache=False,
        ),
) -> None:
    admins_notification_service = SpecificChatsNotificationService(
        bot=bot,
        chat_ids=admin_user_ids,
    )
    shift_date = datetime.date.fromisoformat(message.web_app_data.data)
    staff = await staff_repository.get_by_id(message.from_user.id)
    view = ExtraShiftScheduleNotificationView(
        staff_id=staff.id,
        staff_full_name=staff.full_name,
        shift_date=shift_date,
    )
    await admins_notification_service.send_view(view)
    await message.answer(
        '✅ Ваш запрос на доп.смену в'
        f' {shift_date:%d.%m.%Y} отправлен на проверку'
    )
    view = MainMenuView(config.web_app_base_url)
    await answer_text_view(message, view)


@router.message(
    F.text == ButtonText.SHIFT_START_EXTRA,
    invert_f(admins_filter),
    StateFilter('*'),
)
async def on_start_extra_shift(message, config: Config):
    view = ExtraShiftScheduleWebAppView(config.web_app_base_url)
    await answer_text_view(message, view)

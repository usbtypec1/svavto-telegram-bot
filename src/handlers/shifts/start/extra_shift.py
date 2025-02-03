import datetime

from aiogram import Bot, F, Router
from aiogram.exceptions import TelegramAPIError
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from fast_depends import Depends, inject

from callback_data import (
    ExtraShiftCreateAcceptCallbackData,
    ExtraShiftCreateRejectCallbackData, ExtraShiftStartCallbackData,
    ShiftStartCarWashCallbackData,
)
from config import Config
from dependencies.repositories import (
    CarWashRepositoryDependency, ShiftRepositoryDependency,
    get_staff_repository,
)
from filters import admins_filter, staff_filter
from repositories import StaffRepository
from services.notifications import SpecificChatsNotificationService
from services.validators import validate_shift_date
from states import ShiftExtraStartStates
from ui.views import (
    ButtonText, ExtraShiftScheduleNotificationView,
    ExtraShiftScheduleWebAppView, MainMenuView,
    ShiftExtraStartRequestConfirmedView, ShiftMenuView,
    ShiftStartCarWashChooseView, answer_text_view, edit_as_rejected,
    edit_message_by_view,
    send_text_view,
)

__all__ = ('router',)

from ui.views.base import edit_as_accepted

router = Router(name=__name__)


@router.callback_query(
    ShiftStartCarWashCallbackData.filter(),
    staff_filter,
    StateFilter(ShiftExtraStartStates.car_wash),
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
        text='✅ Вы начали доп.смену водителя перегонщика на мойку',
    )
    view = ShiftMenuView(
        staff_id=callback_query.from_user.id,
        web_app_base_url=config.web_app_base_url,
    )
    await answer_text_view(callback_query.message, view)
    await callback_query.answer()


@router.callback_query(
    ExtraShiftStartCallbackData.filter(),
    staff_filter,
    StateFilter('*'),
)
@inject
async def on_extra_shift_start(
        callback_query: CallbackQuery,
        callback_data: ExtraShiftStartCallbackData,
        config: Config,
        state: FSMContext,
        shift_repository: ShiftRepositoryDependency,
        car_wash_repository: CarWashRepositoryDependency,
) -> None:
    shift_date = datetime.date.fromisoformat(callback_data.date)

    validate_shift_date(shift_date=callback_data.date, timezone=config.timezone)

    await state.set_state(ShiftExtraStartStates.car_wash)
    await state.update_data(date=callback_data.date, is_extra=True)
    car_washes = await car_wash_repository.get_all()
    if not car_washes:
        await callback_query.answer(
            text='❌ Нет доступных моек',
            show_alert=True,
        )
        return

    shift_create_result = await shift_repository.create_extra(
        staff_id=callback_query.from_user.id,
        shift_date=shift_date,
    )
    await state.update_data(shift_id=shift_create_result.shift_id)
    await state.set_state(ShiftExtraStartStates.car_wash)
    view = ShiftStartCarWashChooseView(car_washes)
    await edit_message_by_view(callback_query.message, view)


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
    view = ShiftExtraStartRequestConfirmedView(
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
        await edit_as_accepted(callback_query.message)


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
        await edit_as_rejected(callback_query.message)


@router.message(
    F.web_app_data.button_text == ButtonText.EXTRA_SHIFT_CALENDAR,
    staff_filter,
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
    staff_filter,
    StateFilter('*'),
)
async def on_start_extra_shift(message, config: Config):
    view = ExtraShiftScheduleWebAppView(config.web_app_base_url)
    await answer_text_view(message, view)

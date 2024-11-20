import datetime

from aiogram import Bot, F, Router
from aiogram.filters import StateFilter, invert_f
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from fast_depends import Depends, inject

from callback_data import (
    ShiftStartCallbackData,
    ShiftStartCarWashCallbackData,
    ShiftWorkTypeChoiceCallbackData,
)
from config import Config
from dependencies.repositories import (
    get_car_wash_repository,
    get_shift_repository,
)
from enums import ShiftWorkType
from filters import admins_filter
from models import ShiftsConfirmation, Staff
from repositories import CarWashRepository, ShiftRepository
from services.notifications import SpecificChatsNotificationService
from states import ShiftStartStates
from views.base import answer_view, edit_message_by_view, send_view
from views.button_texts import ButtonText
from views.menu import ShiftMenuView
from views.shifts import (
    ShiftImmediateStartRequestView, ShiftStartCarWashChooseView,
    ShiftStartConfirmView,
    ShiftStartRequestView, ShiftWorkTypeChoiceView,
)

__all__ = ('router',)

router = Router(name=__name__)


@router.callback_query(
    ShiftStartCarWashCallbackData.filter(),
    invert_f(admins_filter),
    StateFilter(ShiftStartStates.car_wash),
)
@inject
async def on_start_shift_car_wash(
        callback_query: CallbackQuery,
        callback_data: ShiftStartCarWashCallbackData,
        state: FSMContext,
        config: Config,
        shift_repository: ShiftRepository = Depends(
            dependency=get_shift_repository,
            use_cache=False,
        ),
) -> None:
    state_data: dict = await state.get_data()
    await state.clear()
    if (shift_date := state_data.get('date')) is not None:
        await shift_repository.create(
            staff_id=callback_query.from_user.id,
            car_wash_id=callback_data.car_wash_id,
            dates=[datetime.date.fromisoformat(shift_date)],
            immediate_start=True,
            is_extra=state_data.get('is_extra', False),
        )
    else:
        shift_id: int = state_data['shift_id']
        await shift_repository.start(
            shift_id=shift_id,
            car_wash_id=callback_data.car_wash_id,
        )
    await callback_query.message.edit_text(
        text='✅ Вы начали смену водителя перегонщика на мойку',
    )
    view = ShiftMenuView(
        staff_id=callback_query.from_user.id,
        web_app_base_url=config.web_app_base_url,
    )
    await answer_view(callback_query.message, view)


@router.callback_query(
    ShiftStartCallbackData.filter(),
    invert_f(admins_filter),
    StateFilter('*'),
)
@inject
async def on_start_shift(
        callback_query: CallbackQuery,
        callback_data: ShiftStartCallbackData,
        state: FSMContext,
        car_wash_repository: CarWashRepository = Depends(
            dependency=get_car_wash_repository,
            use_cache=False,
        ),
) -> None:
    car_washes = await car_wash_repository.get_all()
    if not car_washes:
        await callback_query.answer(
            text='❌ Нет доступных моек',
            show_alert=True,
        )
        return
    await state.update_data(shift_id=callback_data.shift_id)
    await state.set_state(ShiftStartStates.car_wash)
    view = ShiftStartCarWashChooseView(car_washes)
    await edit_message_by_view(callback_query.message, view)


@router.message(
    F.web_app_data.button_text == ButtonText.SHIFTS_TODAY,
    admins_filter,
    StateFilter('*'),
)
@inject
async def on_send_confirmation_to_staff(
        message: Message,
        bot: Bot,
        shift_repository: ShiftRepository = Depends(
            dependency=get_shift_repository,
            use_cache=False,
        ),
) -> None:
    shifts_confirmation = ShiftsConfirmation.model_validate_json(
        json_data=message.web_app_data.data,
    )
    shifts_page = await shift_repository.get_list(
        staff_ids=shifts_confirmation.staff_ids,
        limit=1000,
    )
    shifts = shifts_page.shifts

    staff_id_to_shift = {shift.staff.id: shift for shift in shifts}

    await message.answer('Отправляю запросы на начало смены')

    count = 0
    for staff_id in shifts_confirmation.staff_ids:
        try:
            shift = staff_id_to_shift[staff_id]
        except KeyError:
            view = ShiftImmediateStartRequestView(date=shifts_confirmation.date)
        else:
            view = ShiftStartConfirmView(
                shift_id=shift.id,
                staff_full_name=shift.staff.full_name,
            )
        finally:
            count += 1
        await send_view(bot, view, staff_id)

    await message.answer(
        f'✅ Запросы на начало смены отправлены {count} сотрудникам',
    )


@router.callback_query(
    ShiftWorkTypeChoiceCallbackData.filter(
        rule=F.work_type == ShiftWorkType.MOVE_TO_WASH,
    ),
    invert_f(admins_filter),
    StateFilter('*'),
)
@inject
async def on_move_to_wash_shift_work_type_choice(
        callback_query: CallbackQuery,
        config: Config,
        staff: Staff,
        admins_notification_service: SpecificChatsNotificationService,
        shift_repository: ShiftRepository = Depends(
            dependency=get_shift_repository,
            use_cache=False,
        ),
) -> None:
    now = datetime.datetime.now(config.timezone)
    shifts_page = await shift_repository.get_list(
        date_from=now,
        date_to=now,
        staff_ids=[staff.id],
    )
    if not shifts_page.shifts:
        await callback_query.answer(
            text='❌У вас нет на сегодня смены',
            show_alert=True
        )
        return
    shift = shifts_page.shifts[0]
    view = ShiftStartRequestView(shift=shift, staff=staff)
    await admins_notification_service.send_view(view)
    await callback_query.message.edit_text(
        'До 21:30 Вам придет уведомление в этот бот с запросом'
        ' <b>подтвердить или отклонить</b> выход на смену.'
        '\nПосле подтверждения, смена автоматически начнется.'
    )


@router.callback_query(
    ShiftWorkTypeChoiceCallbackData.filter(),
    invert_f(admins_filter),
    StateFilter('*'),
)
async def on_shift_work_type_choice(callback_query: CallbackQuery) -> None:
    await callback_query.answer('В разработке', show_alert=True)


@router.message(
    F.text == ButtonText.SHIFT_START,
    invert_f(admins_filter),
    StateFilter('*'),
)
async def on_show_shift_work_types_list(
        message: Message,
) -> None:
    await answer_view(message, ShiftWorkTypeChoiceView())

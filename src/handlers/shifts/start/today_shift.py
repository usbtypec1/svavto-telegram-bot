from aiogram import F, Router
from aiogram.filters import StateFilter, invert_f
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from fast_depends import inject

from callback_data import (
    ShiftStartCarWashCallbackData,
    ShiftWorkTypeChoiceCallbackData,
)
from config import Config
from dependencies.repositories import (
    CarWashRepositoryDependency, ShiftRepositoryDependency,
)
from enums import ShiftWorkType
from filters import admins_filter
from logger import create_logger
from models import Staff
from services.shifts import (
    get_current_shift_date,
    is_time_to_start_shift,
)
from states import ShiftRegularStartStates
from ui.views import (
    ButtonText, ShiftMenuView, ShiftStartCarWashChooseView,
    ShiftWorkTypeChoiceView, answer_text_view, edit_message_by_view,
)

__all__ = ('router',)

logger = create_logger(__name__)

router = Router(name=__name__)


@router.callback_query(
    ShiftStartCarWashCallbackData.filter(),
    StateFilter(ShiftRegularStartStates.car_wash),
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
        text='✅ Вы начали смену водителя перегонщика на мойку',
    )
    view = ShiftMenuView(
        staff_id=callback_query.from_user.id,
        web_app_base_url=config.web_app_base_url,
    )
    await answer_text_view(callback_query.message, view)
    await callback_query.answer()


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
        state: FSMContext,
        shift_repository: ShiftRepositoryDependency,
        car_wash_repository: CarWashRepositoryDependency,
) -> None:
    shift_date = get_current_shift_date(config.timezone)
    logger.debug(
        'Trying to start car transporter shift for date %s',
        shift_date,
    )
    shifts_page = await shift_repository.get_list(
        date_from=shift_date,
        date_to=shift_date,
        staff_ids=[staff.id],
    )
    logger.info('Shifts for date %s: %s', shift_date, shifts_page.shifts)
    if not shifts_page.shifts:
        await callback_query.answer(
            text='❌У вас нет на сегодня смены',
            show_alert=True
        )
        return

    if not is_time_to_start_shift(config.timezone):
        await callback_query.message.answer(
            text=(
                'До 21:30 Вам придет уведомление в этот бот с запросом'
                ' <b>подтвердить или отклонить</b> выход на смену.'
                '\nПосле подтверждения, смена автоматически начнется.'
            ),
        )
        return

    shift = shifts_page.shifts[0]

    car_washes = await car_wash_repository.get_all()
    if not car_washes:
        await callback_query.answer(
            text='❌ Нет доступных моек',
            show_alert=True,
        )
        return
    await state.update_data(shift_id=shift.id)
    await state.set_state(ShiftRegularStartStates.car_wash)
    view = ShiftStartCarWashChooseView(car_washes)
    await edit_message_by_view(callback_query.message, view)


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
    await answer_text_view(message, ShiftWorkTypeChoiceView())

import datetime

from aiogram import Bot, F, Router
from aiogram.filters import StateFilter, invert_f
from aiogram.types import CallbackQuery, Message
from fast_depends import Depends, inject

from callback_data import ShiftWorkTypeChoiceCallbackData
from config import Config
from dependencies.repositories import get_shift_repository
from enums import ShiftWorkType
from filters import admins_filter
from models import Staff
from repositories import ShiftRepository
from services.notifications import SpecificChatsNotificationService
from views.base import answer_view
from views.button_texts import ButtonText
from views.shifts import ShiftStartRequestView, ShiftWorkTypeChoiceView

__all__ = ('router',)

router = Router(name=__name__)


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
        bot: Bot,
        admin_user_ids: set[int],
        shift_repository: ShiftRepository = Depends(
            dependency=get_shift_repository,
            use_cache=False,
        ),
) -> None:
    admins_notification_service = SpecificChatsNotificationService(
        bot=bot,
        chat_ids=admin_user_ids,
    )
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

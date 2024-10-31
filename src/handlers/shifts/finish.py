from aiogram import F, Router
from aiogram.filters import StateFilter, invert_f
from aiogram.types import CallbackQuery, Message
from fast_depends import Depends, inject

from callback_data.prefixes import CallbackDataPrefix
from config import Config
from dependencies.repositories import get_shift_repository
from filters import admins_filter
from repositories import ShiftRepository
from views.base import answer_view, edit_message_by_view
from views.button_texts import ButtonText
from views.menu import StaffShiftCarWashMenuView
from views.shifts import ShiftFinishConfirmView

__all__ = ('router',)

router = Router(name=__name__)


@router.callback_query(
    F.data == CallbackDataPrefix.SHIFT_FINISH_REJECT,
    invert_f(admins_filter),
    StateFilter('*'),
)
@inject
async def on_shift_finish_reject(
        callback_query: CallbackQuery,
        config: Config,
        shift_repository: ShiftRepository = Depends(
            get_shift_repository,
            use_cache=False,
        ),
) -> None:
    await shift_repository.get_active(callback_query.from_user.id)
    view = StaffShiftCarWashMenuView(config.web_app_base_url)
    await answer_view(callback_query.message, view)
    await callback_query.answer(
        text='❗️ Вы отменили завершение смены',
        show_alert=True,
    )
    await callback_query.message.delete()


@router.message(
    F.text == ButtonText.SHIFT_END,
    invert_f(admins_filter),
    StateFilter('*'),
)
@inject
async def on_shift_finish_confirm(
        message: Message,
        shift_repository: ShiftRepository = Depends(
            get_shift_repository,
            use_cache=False,
        ),
) -> None:
    await shift_repository.get_active(message.from_user.id)
    view = ShiftFinishConfirmView()
    await answer_view(message, view)

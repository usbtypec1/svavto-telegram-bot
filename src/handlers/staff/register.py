from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery
from fast_depends import inject, Depends

from callback_data.prefixes import CallbackDataPrefix
from config import Config
from dependencies.repositories import get_staff_repository
from exceptions import StaffNotFoundError, StaffAlreadyExistsError
from filters import admins_filter
from repositories import StaffRepository
from services.staff import parse_staff_register_text
from ui.views import edit_as_accepted, edit_as_rejected, send_text_view
from ui.views import MainMenuView
from ui.views import StaffRegisterAcceptedView, StaffRegisterRejectedView

__all__ = ('router',)

router = Router(name=__name__)


@router.callback_query(
    F.data == CallbackDataPrefix.STAFF_REGISTER_REJECT,
    admins_filter,
    StateFilter('*'),
)
@inject
async def on_staff_register_reject(
        callback_query: CallbackQuery,
        bot: Bot,
        staff_repository: StaffRepository = Depends(
            dependency=get_staff_repository,
            use_cache=False,
        ),
) -> None:
    message_text = callback_query.message.text
    staff_to_register = parse_staff_register_text(message_text)
    try:
        await staff_repository.get_by_id(staff_to_register.id)
    except StaffNotFoundError:
        await callback_query.answer('❌ Отклонено', show_alert=True)
        await edit_as_rejected(callback_query.message)
        view = StaffRegisterRejectedView()
        await send_text_view(bot, view, staff_to_register.id)
    else:
        raise StaffAlreadyExistsError


@router.callback_query(
    F.data == CallbackDataPrefix.STAFF_REGISTER_ACCEPT,
    admins_filter,
    StateFilter('*'),
)
@inject
async def on_staff_register_accept(
        callback_query: CallbackQuery,
        bot: Bot,
        config: Config,
        staff_repository: StaffRepository = Depends(
            dependency=get_staff_repository,
            use_cache=False,
        ),
) -> None:
    message_text = callback_query.message.text
    staff_to_register = parse_staff_register_text(message_text)

    try:
        await staff_repository.create(staff_to_register)
    except StaffAlreadyExistsError:
        await callback_query.answer(
            '❌ Пользователь уже зарегистрирован',
            show_alert=True,
        )
        await edit_as_rejected(
            message=callback_query.message,
            detail='Пользователь уже зарегистрирован',
        )
        return

    staff = await staff_repository.get_by_id(staff_to_register.id)
    await edit_as_accepted(callback_query.message)
    await callback_query.answer(
        '✅ Заявка на регистрацию принята',
        show_alert=True,
    )
    view = StaffRegisterAcceptedView()
    await send_text_view(bot, view, staff.id)
    view = MainMenuView(
        staff_id=callback_query.from_user.id,
        web_app_base_url=config.web_app_base_url,
    )
    await send_text_view(bot, view, staff.id)

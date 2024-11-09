from aiogram import Router, F
from aiogram.filters import ExceptionTypeFilter, StateFilter
from aiogram.types import ErrorEvent, Message, ReplyKeyboardRemove
from fast_depends import Depends, inject

from config import Config
from dependencies.repositories import get_staff_repository
from exceptions import StaffRegisterTextParseError, StaffAlreadyExistsError, \
    StaffNotFoundError
from models import StaffToRegister
from repositories import StaffRepository
from services.notifications import (
    NotificationService,
    SpecificChatsNotificationService,
)
from services.telegram_events import answer_appropriate_event

__all__ = ('router',)

from views.button_texts import ButtonText
from views.register import StaffRegisterNotificationView

router = Router(name=__name__)


@router.error(ExceptionTypeFilter(StaffAlreadyExistsError))
async def on_staff_already_exists_error(event: ErrorEvent) -> None:
    text = 'Сотрудник уже зарегистрирован'
    await answer_appropriate_event(event, text)


@router.error(ExceptionTypeFilter(StaffRegisterTextParseError))
async def on_staff_register_text_parse_error(event: ErrorEvent) -> None:
    text = (
        'Ошибка в форме заявки на регистрацию.'
        ' Попросите пользователя отправить заявку снова'
    )
    await answer_appropriate_event(event, text)


@router.message(
    F.web_app_data.button_text == ButtonText.REGISTER,
    StateFilter('*'),
)
@inject
async def on_register_form_filled(
        message: Message,
        config: Config,
        admins_notification_service: SpecificChatsNotificationService,
        staff_repository: StaffRepository = Depends(
            dependency=get_staff_repository,
            use_cache=False,
        ),

) -> None:
    try:
        await staff_repository.get_by_id(message.from_user.id)
    except StaffNotFoundError:
        staff = StaffToRegister.model_validate_json(message.web_app_data.data)
        view = StaffRegisterNotificationView(staff, message.from_user.id)
        await admins_notification_service.send_view(view=view)
        await message.answer(
            '✅ Ваша заявка на регистрацию отправлена на проверку',
            reply_markup=ReplyKeyboardRemove(),
        )
    else:
        await message.answer('❗️ Вы уже зарегистрированы')

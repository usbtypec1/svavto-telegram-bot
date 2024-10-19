from aiogram import Router, F
from aiogram.filters import StateFilter, ExceptionTypeFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ForceReply, ErrorEvent
from fast_depends import Depends, inject

from callback_data.prefixes import CallbackDataPrefix
from dependencies.repositories import get_staff_repository
from exceptions import StaffRegisterTextParseError, StaffAlreadyExistsError
from models import StaffToCreate
from repositories import StaffRepository
from services import NotificationService
from services.staff import parse_staff_register_text
from services.telegram_events import answer_appropriate_event
from states import StaffRegisterStates
from views.base import answer_view
from views.register import StaffRegisterConfirmView

__all__ = ('router',)

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


@router.callback_query(
    F.data == CallbackDataPrefix.STAFF_REGISTER_REJECT,
    StateFilter('*'),
)
async def on_staff_register_reject(callback_query: CallbackQuery) -> None:
    staff = parse_staff_register_text(callback_query.message.text)
    await callback_query.message.edit_text(
        f'{callback_query.message.text}'
        f'\n\n<i>❌ Заявка на регистрацию отменена</i>'
    )


@router.callback_query(
    F.data == CallbackDataPrefix.STAFF_REGISTER_ACCEPT,
    StateFilter('*'),
)
@inject
async def on_staff_register_accept(
        callback_query: CallbackQuery,
        staff_repository: StaffRepository = Depends(
            dependency=get_staff_repository,
            use_cache=False,
        ),
) -> None:
    staff = parse_staff_register_text(callback_query.message.text)
    staff = await staff_repository.create(staff)
    await callback_query.message.edit_text(
        f'{callback_query.message.text}'
        f'\n\n<i>✅ Сотрудник успешно зарегистрирован</i>'
    )


@router.callback_query(
    F.data == 'register-confirm',
    StateFilter(StaffRegisterStates.console_phone_number),
)
async def on_performer_register_confirm(
        callback_query: CallbackQuery,
        state: FSMContext,
        notification_service: NotificationService,
        admin_user_ids: set[int],
) -> None:
    state_data = await state.get_data()
    await state.clear()
    full_name: str = state_data['full_name']
    car_sharing_phone_number: str = state_data['car_sharing_phone_number']
    console_phone_number: str = state_data['console_phone_number']
    staff = StaffToCreate(
        id=callback_query.from_user.id,
        full_name=full_name,
        car_sharing_phone_number=car_sharing_phone_number,
        console_phone_number=console_phone_number,
    )
    await notification_service.send_new_user_notification(
        admin_user_ids=admin_user_ids,
        staff=staff,
    )


@router.message(
    F.text,
    StateFilter(StaffRegisterStates.console_phone_number),
)
async def on_console_phone_number_input(
        message: Message,
        state: FSMContext,
) -> None:
    state_data = await state.get_data()
    await state.update_data(console_phone_number=message.text)
    view = StaffRegisterConfirmView(
        full_name=state_data['full_name'],
        car_sharing_phone_number=state_data['car_sharing_phone_number'],
        console_phone_number=message.text,
    )
    await answer_view(message, view)


@router.message(
    F.text,
    StateFilter(StaffRegisterStates.car_sharing_phone_number),
)
async def on_car_sharing_phone_number_input(
        message: Message,
        state: FSMContext,
) -> None:
    await state.update_data(car_sharing_phone_number=message.text)
    await state.set_state(StaffRegisterStates.console_phone_number)
    await message.answer(
        'Введите номер телефона, указанный в компании Консоль:',
        reply_markup=ForceReply(input_field_placeholder='Номер телефона'),
    )


@router.message(
    F.text,
    StateFilter(StaffRegisterStates.full_name),
)
async def on_full_name_input(message: Message, state: FSMContext) -> None:
    await state.update_data(full_name=message.text)
    await state.set_state(StaffRegisterStates.car_sharing_phone_number)
    await message.answer(
        'Введите номер телефона, привязанный к аккаунту в каршеринге:',
        reply_markup=ForceReply(input_field_placeholder='Номер телефона'),
    )


@router.callback_query(
    F.data == 'register',
    StateFilter('*'),
)
async def on_start_registration(
        callback_query: CallbackQuery,
        state: FSMContext,
) -> None:
    await state.set_state(StaffRegisterStates.full_name)
    await callback_query.message.answer(
        'Введите ваше ФИО:',
        reply_markup=ForceReply(input_field_placeholder='ФИО'),
    )

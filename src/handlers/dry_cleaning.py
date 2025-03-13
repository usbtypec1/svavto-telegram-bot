import re

from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from fast_depends import inject
from pydantic import TypeAdapter

from callback_data.prefixes import CallbackDataPrefix
from config import Config
from dependencies.repositories import (
    DryCleaningRequestRepositoryDependency, ShiftRepositoryDependency,
)
from filters import staff_filter
from models.dry_cleaning_requests import DryCleaningRequestServiceWithName
from services.photos_storage import PhotosStorage
from states import DryCleaningRequestStates
from ui.views import (
    answer_view, ButtonText, DryCleaningCarNumberView,
    DryCleaningRequestConfirmView, DryCleaningRequestPhotoInputView,
    DryCleaningRequestPhotosView, DryCleaningRequestPhotoUploadView,
    DryCleaningRequestServicesView, edit_as_confirmed, edit_as_rejected,
    ShiftMenuView,
)


router = Router(name=__name__)


@router.message(
    F.text == ButtonText.SHIFT_DRY_CLEANING_REQUEST,
    staff_filter,
    StateFilter('*'),
)
@inject
async def on_dry_cleaning_request_start_flow(
        message: Message,
        state: FSMContext,
        photos_storage: PhotosStorage,
        shift_repository: ShiftRepositoryDependency,
) -> None:
    await photos_storage.clear()

    shift = await shift_repository.get_active(message.from_user.id)
    if shift.car_wash is None:
        await message.reply(
            text='❗️ Выберите мойку на которой будете работать',
        )
        return
    transferred_cars_response = await shift_repository.get_transferred_cars(
        shift_id=shift.id,
    )
    await state.set_state(DryCleaningRequestStates.car_number)
    await state.update_data(car_wash_id=shift.car_wash.id, shift_id=shift.id)
    car_numbers = [
        car.number for car in transferred_cars_response.transferred_cars
    ]
    view = DryCleaningCarNumberView(car_numbers)
    await answer_view(message, view)


@router.callback_query(
    F.data == CallbackDataPrefix.CAR_NUMBER_INPUT,
    staff_filter,
    StateFilter(DryCleaningRequestStates.car_number),
)
async def on_car_number_manual_input(callback_query: CallbackQuery) -> None:
    await callback_query.message.answer(
        text='Введите номер автомобиля',
    )


def is_car_number_valid(car_number: str) -> bool:
    pattern = r'^[А-Яа-я]\d{3}[А-Яа-я]{2}\d{3}$'
    return bool(re.fullmatch(pattern, car_number))


@router.message(
    F.text,
    staff_filter,
    StateFilter(DryCleaningRequestStates.car_number),
)
async def on_car_number_input(
        message: Message,
        state: FSMContext,
) -> None:
    if not is_car_number_valid(message.text):
        await message.reply(
            text='❗️ Введите номер автомобиля в формате "а123бв123"',
        )
    else:
        await state.update_data(car_number=message.text)
        await state.set_state(DryCleaningRequestStates.photos)
        view = DryCleaningRequestPhotoInputView()
        await answer_view(message, view)


@router.callback_query(
    staff_filter,
    StateFilter(DryCleaningRequestStates.car_number),
)
async def on_choose_car(
        callback_query: CallbackQuery,
        state: FSMContext,
):
    await state.update_data(car_number=callback_query.data)
    await state.set_state(DryCleaningRequestStates.photos)
    view = DryCleaningRequestPhotoInputView()
    await answer_view(callback_query.message, view)


@router.message(
    staff_filter,
    F.photo,
    StateFilter(DryCleaningRequestStates.photos),
)
async def on_photo_input(
        message: Message,
        photos_storage: PhotosStorage,
) -> None:
    file_id = message.photo[-1].file_id
    count = await photos_storage.count()
    if count > 10:
        await message.reply(
            text='❗️ Вы не можете загрузить больше 10 фотографий',
        )
        return
    await photos_storage.add_file_id(file_id)
    view = DryCleaningRequestPhotoUploadView(photo_file_id=file_id)
    await answer_view(message, view)


@router.callback_query(
    staff_filter,
    F.data == CallbackDataPrefix.DRY_CLEANING_REQUEST_PHOTO_DELETE,
    StateFilter(DryCleaningRequestStates.photos),
)
async def on_photo_delete(
        callback_query: CallbackQuery,
        photos_storage: PhotosStorage,
) -> None:
    file_id = callback_query.message.photo[-1].file_id
    await photos_storage.delete_file_id(file_id)
    await callback_query.answer(text='❗️ Фотография удалена', show_alert=True)
    await callback_query.message.delete()


@router.message(
    staff_filter,
    F.text == ButtonText.DRY_CLEANING_REQUEST_PHOTO_INPUT_FINISH,
    StateFilter(DryCleaningRequestStates.photos),
)
async def on_photo_input_finish(
        message: Message,
        state: FSMContext,
        config: Config,
        photos_storage: PhotosStorage,
) -> None:
    count = await photos_storage.count()
    if count == 0:
        view = DryCleaningRequestPhotoInputView()
        await answer_view(message, view)
        return

    await state.set_state(DryCleaningRequestStates.services)
    state_data: dict = await state.get_data()
    car_wash_id: int = state_data['car_wash_id']
    view = DryCleaningRequestServicesView(
        web_app_base_url=config.web_app_base_url,
        car_wash_id=car_wash_id,
    )
    await answer_view(message, view)


@router.message(
    staff_filter,
    F.web_app_data.button_text == ButtonText.DRY_CLEANING_REQUEST_SERVICES,
    StateFilter(DryCleaningRequestStates.services),
)
async def on_services_input(
        message: Message,
        state: FSMContext,
        photos_storage: PhotosStorage,
) -> None:
    await state.update_data(services=message.web_app_data.data)
    await state.set_state(DryCleaningRequestStates.confirm)
    photo_file_ids = await photos_storage.get_file_ids()

    type_adapter = TypeAdapter(tuple[DryCleaningRequestServiceWithName, ...])
    state_data: dict = await state.get_data()
    car_number: str = state_data['car_number']
    services_json: str = state_data['services']
    services = type_adapter.validate_json(services_json)

    view = DryCleaningRequestPhotosView(
        car_number=car_number,
        services=services,
        photo_file_ids=photo_file_ids,
    )
    await answer_view(message, view)

    view = DryCleaningRequestConfirmView()
    await answer_view(message, view)


@router.callback_query(
    staff_filter,
    F.data == CallbackDataPrefix.DRY_CLEANING_REQUEST_REJECT,
    StateFilter(DryCleaningRequestStates.confirm),
)
async def on_dry_cleaning_request_reject(
        callback_query: CallbackQuery,
        state: FSMContext,
        photos_storage: PhotosStorage,
        config: Config,
) -> None:
    await photos_storage.clear()
    await state.clear()
    await edit_as_rejected(callback_query.message)
    await callback_query.answer()
    view = ShiftMenuView(
        staff_id=callback_query.from_user.id,
        web_app_base_url=config.web_app_base_url,
    )
    await answer_view(callback_query.message, view)


@router.callback_query(
    staff_filter,
    F.data == CallbackDataPrefix.DRY_CLEANING_REQUEST_CONFIRM,
    StateFilter(DryCleaningRequestStates.confirm),
)
@inject
async def on_dry_cleaning_request_confirm(
        callback_query: CallbackQuery,
        state: FSMContext,
        photos_storage: PhotosStorage,
        config: Config,
        dry_cleaning_request_repository: (
                DryCleaningRequestRepositoryDependency
        ),
) -> None:
    photo_file_ids = await photos_storage.get_file_ids()

    type_adapter = TypeAdapter(tuple[DryCleaningRequestServiceWithName, ...])
    state_data: dict = await state.get_data()
    car_number: str = state_data['car_number']
    services_json: str = state_data['services']
    shift_id: int = state_data['shift_id']
    services = type_adapter.validate_json(services_json)

    await edit_as_confirmed(callback_query.message)
    await dry_cleaning_request_repository.create(
        shift_id=shift_id,
        car_number=car_number,
        photo_file_ids=photo_file_ids,
        services=services,
    )
    await callback_query.answer('✅ Заявка создана', show_alert=True)

    view = ShiftMenuView(
        staff_id=callback_query.from_user.id,
        web_app_base_url=config.web_app_base_url,
    )
    await answer_view(callback_query.message, view)

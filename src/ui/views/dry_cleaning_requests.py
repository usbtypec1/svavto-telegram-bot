from collections.abc import Iterable

from aiogram.types import (
    InlineKeyboardButton, InlineKeyboardMarkup,
    InputMediaPhoto, KeyboardButton, ReplyKeyboardMarkup, WebAppInfo,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.media_group import MediaType

from callback_data.prefixes import CallbackDataPrefix
from models.dry_cleaning_requests import DryCleaningRequestServiceWithName
from ui.markups import create_confirm_reject_markup
from ui.views import ButtonText, MediaGroupView, PhotoView, TextView


class DryCleaningCarNumberView(TextView):
    text = 'Выберите номер машины, для которой запрашиваете химчистку'

    def __init__(self, car_numbers: Iterable[str]):
        self.__car_numbers = tuple(car_numbers)

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardBuilder()
        keyboard.max_width = 1

        for car_number in self.__car_numbers:
            keyboard.button(text=car_number, callback_data=car_number)

        keyboard.button(
            text='📝 Ввести вручную',
            callback_data=CallbackDataPrefix.CAR_NUMBER_INPUT,
        )

        return keyboard.as_markup()


class DryCleaningRequestPhotoUploadView(PhotoView):
    caption = (
        '✅ Фотография принята\n'
        'Вы можете отправить ещё фото'
    )

    def __init__(self, photo_file_id: str):
        self.__photo_file_id = photo_file_id

    def get_photo(self) -> str:
        return self.__photo_file_id

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        photo_delete_button = InlineKeyboardButton(
            text='❌ Удалить фото',
            callback_data=CallbackDataPrefix.DRY_CLEANING_REQUEST_PHOTO_DELETE,
        )
        return InlineKeyboardMarkup(inline_keyboard=[[photo_delete_button]])


class DryCleaningRequestPhotoInputView(TextView):
    text = '🖼️ Загрузите фотографии загрязненных элементов'
    reply_markup = ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True,
        keyboard=[
            [
                KeyboardButton(
                    text=ButtonText.DRY_CLEANING_REQUEST_PHOTO_INPUT_FINISH,
                ),
            ],
        ],
    )


class DryCleaningRequestServicesView(TextView):
    text = '🫧 Выберите услуги'

    def __init__(self, web_app_base_url: str, car_wash_id: int):
        self.__web_app_base_url = web_app_base_url
        self.__car_wash_id = car_wash_id

    def get_reply_markup(self) -> ReplyKeyboardMarkup:
        button = KeyboardButton(
            text=ButtonText.DRY_CLEANING_REQUEST_SERVICES,
            web_app=WebAppInfo(
                url=(
                    f'{self.__web_app_base_url}'
                    f'/car-washes/{self.__car_wash_id}/dry-cleaning'
                ),
            )
        )
        return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[[button]])


class DryCleaningRequestPhotosView(MediaGroupView):

    def __init__(
            self,
            *,
            car_number: str,
            photo_file_ids: Iterable[str],
            services: Iterable[DryCleaningRequestServiceWithName],
    ):
        self.__car_number = car_number
        self.__photo_file_ids = tuple(photo_file_ids)
        self.__services = tuple(services)

    def get_caption(self) -> str:
        lines: list[str] = [
            f'🚗 Номер машины: {self.__car_number}',
            '',
            '<b>Список услуг:</b>'
        ]

        for service in self.__services:
            lines.append(f'🫧 {service.name} - {service.count}')

        return '\n'.join(lines)

    def get_medias(self) -> list[MediaType] | None:
        return [
            InputMediaPhoto(media=photo_file_id)
            for photo_file_id in self.__photo_file_ids
        ]


class DryCleaningRequestConfirmView(TextView):
    text = '❗️ Вы уверены, что хотите отправить заявку на химчистку?'
    reply_markup = create_confirm_reject_markup(
        confirm_callback_data=CallbackDataPrefix.DRY_CLEANING_REQUEST_CONFIRM,
        reject_callback_data=CallbackDataPrefix.DRY_CLEANING_REQUEST_REJECT,
    )

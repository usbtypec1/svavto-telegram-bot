from collections.abc import Iterable

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaPhoto,
    KeyboardButton,
    ReplyKeyboardMarkup,
)
from aiogram.utils.media_group import MediaType

import ui.markups
from callback_data.prefixes import CallbackDataPrefix
from models import ShiftFinishCarWashSummary, ShiftFinishResult
from ui.views.base import MediaGroupView, TextView, PhotoView
from ui.views.button_texts import ButtonText

__all__ = (
    'ShiftFinishConfirmView',
    'StaffShiftFinishedView',
    'ShiftFinishPhotosView',
    'ShiftFinishedWithPhotosView',
    'ShiftFinishPhotoConfirmView',
    'ShiftFinishConfirmAllView',
    'StaffFirstShiftFinishedView',
    'ShiftFinishedWithoutPhotosView',
    'format_shift_finish_text',
    'format_shift_car_wash_finish_summary',
)


class ShiftFinishConfirmView(TextView):
    text = 'Подтверждаете завершение смены?'
    reply_markup = ui.markups.create_confirm_reject_markup(
        accept_callback_data=CallbackDataPrefix.SHIFT_FINISH_FLOW_START_ACCEPT,
        reject_callback_data=CallbackDataPrefix.SHIFT_FINISH_FLOW_START_REJECT,
    )


class ShiftFinishPhotoConfirmView(PhotoView):
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
            callback_data=CallbackDataPrefix.SHIFT_FINISH_PHOTO_DELETE,
        )
        next_step_button = InlineKeyboardButton(
            text='🔜 Следующий шаг',
            callback_data=CallbackDataPrefix.SHIFT_FINISH_PHOTO_NEXT_STEP,
        )
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [photo_delete_button],
                [next_step_button],
            ],
        )


class ShiftFinishPhotosView(MediaGroupView):
    caption = 'Проверьте правильность отправляемых данных'

    def __init__(self, photo_file_ids: Iterable[str]):
        self.__photo_file_ids = tuple(photo_file_ids)

    def get_medias(self) -> list[MediaType]:
        return [
            InputMediaPhoto(
                media=photo_file_id,
            )
            for photo_file_id in self.__photo_file_ids
        ]


class ShiftFinishConfirmAllView(TextView):
    text = 'Подтверждаете завершение смены?'
    reply_markup = ui.markups.create_confirm_reject_markup(
        accept_callback_data=CallbackDataPrefix.SHIFT_FINISH_ACCEPT,
        reject_callback_data=CallbackDataPrefix.SHIFT_FINISH_REJECT,
    )


def format_shift_car_wash_finish_summary(
        car_wash_summary: ShiftFinishCarWashSummary,
) -> str:
    return (
        f'\nМойка: {car_wash_summary.car_wash_name}'
        f'\nВсего: {car_wash_summary.total_cars_count}'
        f'\n🔶 Комфорт: {car_wash_summary.comfort_cars_count}'
        f'\n🔶 Бизнес: {car_wash_summary.business_cars_count}'
        f'\n🔶 Фургон: {car_wash_summary.vans_count}'
        f'\nПлановая мойка: {car_wash_summary.planned_cars_count}'
        f'\nСрочная мойка: {car_wash_summary.urgent_cars_count}'
        f'\nХимчистки: {car_wash_summary.dry_cleaning_count}'
        f'\nДолив: {car_wash_summary.refilled_cars_count}'
        f'\nНедолив: {car_wash_summary.not_refilled_cars_count}'
    )


def format_shift_finish_text(shift_summary: ShiftFinishResult) -> str:
    lines: list[str] = [f'Перегонщик: {shift_summary.staff_full_name}']
    for car_wash_summary in shift_summary.car_washes:
        lines.append(format_shift_car_wash_finish_summary(car_wash_summary))
    if not shift_summary.car_washes:
        lines.append('\nНет добавленных авто')
    return '\n'.join(lines)


class ShiftFinishedWithoutPhotosView(TextView):

    def __init__(self, shift_finish_result: ShiftFinishResult):
        self.__shift_summary = shift_finish_result

    def get_text(self) -> str:
        return format_shift_finish_text(self.__shift_summary)


class ShiftFinishedWithPhotosView(MediaGroupView):

    def __init__(self, shift_finish_result: ShiftFinishResult):
        self.__shift_summary = shift_finish_result

    def get_medias(self) -> list[MediaType] | None:
        return [
            InputMediaPhoto(media=photo_file_id)
            for photo_file_id in self.__shift_summary.finish_photo_file_ids
        ]

    def get_caption(self) -> str:
        return format_shift_finish_text(self.__shift_summary)


class StaffFirstShiftFinishedView(TextView):
    text = (
        'Спасибо за работу! Заполните, пожалуйста, график работы.'
        ' Для этого нажмите на кнопку "График работы" или выберите'
        ' "Сделаю это позже", если хотите заполнить график позже.'
    )
    reply_markup = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [
                KeyboardButton(text=ButtonText.SHIFT_SCHEDULE),
                KeyboardButton(text=ButtonText.LATER)
            ],
        ],
    )


class StaffShiftFinishedView(TextView):
    text = (
        'Проверьте, что все отчеты заполнены верно!'
        ' Спасибо за работу и хорошего дня!'
    )

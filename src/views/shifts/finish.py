from collections.abc import Iterable

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaPhoto,
    KeyboardButton,
    ReplyKeyboardMarkup,
)
from aiogram.utils.media_group import MediaType

from callback_data.prefixes import CallbackDataPrefix
from models import ShiftFinishResult
from views.base import MediaGroupView, TextView
from views.button_texts import ButtonText

__all__ = (
    'ShiftFinishConfirmView',
    'StaffShiftFinishedView',
    'ShiftFinishPhotosView',
    'StaffShiftFinishedNotificationView',
    'ShiftFinishPhotoConfirmView',
    'ShiftFinishConfirmAllView',
    'StaffFirstShiftFinishedView',
)


class ShiftFinishConfirmView(TextView):
    __accept_button = InlineKeyboardButton(
        text='✅ Да',
        callback_data=CallbackDataPrefix.SHIFT_FINISH_FLOW_START_ACCEPT,
    )
    __reject_button = InlineKeyboardButton(
        text='❌ Нет',
        callback_data=CallbackDataPrefix
        .SHIFT_FINISH_FLOW_START_REJECT,
    )
    text = 'Подтверждаете завершение смены?'
    reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[[__accept_button, __reject_button]],
    )


class ShiftFinishPhotoConfirmView(TextView):
    text = (
        '✅ Фотография принята\n'
        'Чтобы заменить фото, отправьте сюда новое'
    )

    def __init__(self, confirm_button_callback_data: str):
        self.__confirm_button_callback_data = confirm_button_callback_data

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text='✅ Подтвердить фото',
                        callback_data=self.__confirm_button_callback_data,
                    )
                ]
            ]
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
    reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='✅ Подтвердить',
                    callback_data=CallbackDataPrefix.SHIFT_FINISH_ACCEPT,
                ),
                InlineKeyboardButton(
                    text='❌ Отменить',
                    callback_data=CallbackDataPrefix.SHIFT_FINISH_REJECT,
                )
            ],
        ],
    )


class StaffShiftFinishedNotificationView(MediaGroupView):

    def __init__(
            self,
            shift_finish_result: ShiftFinishResult,
            photo_file_ids: Iterable[str],
    ):
        self.__shift_finish_result = shift_finish_result
        self.__photo_file_ids = tuple(photo_file_ids)

    def get_medias(self) -> list[MediaType] | None:
        return [
            InputMediaPhoto(media=photo_file_id)
            for photo_file_id in self.__photo_file_ids
        ]

    def get_caption(self) -> str:
        lines: list[str] = [
            f'❗️ Сотрудник {self.__shift_finish_result.staff_full_name}'
            f' завершил смену\n',
        ]

        if self.__shift_finish_result.car_numbers:
            lines.append('🚗 Список добавленных машин:')
        else:
            lines.append('Нет добавленных машин')
        for car_number in self.__shift_finish_result.car_numbers:
            lines.append(car_number)

        return '\n'.join(lines)


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

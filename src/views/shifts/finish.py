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
from views.base import MediaGroupView, TextView, PhotoView
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

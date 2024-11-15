import datetime
from collections.abc import Iterable
from typing import Final
from zoneinfo import ZoneInfo

from aiogram.types import (
    InlineKeyboardButton, InlineKeyboardMarkup,
    InputMediaPhoto, KeyboardButton, ReplyKeyboardMarkup, WebAppInfo,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.media_group import MediaType

from callback_data import (
    ExtraShiftCreateAcceptCallbackData,
    ExtraShiftCreateRejectCallbackData,
    ExtraShiftStartCallbackData,
    ShiftApplyCallbackData,
    ShiftImmediateStartCallbackData, ShiftRejectCallbackData,
    ShiftStartCallbackData,
    ShiftStartCarWashCallbackData,
    ShiftStartRequestAcceptCallbackData,
    ShiftStartRequestRejectCallbackData,
    ShiftWorkTypeChoiceCallbackData,
)
from callback_data.prefixes import CallbackDataPrefix
from callback_data.shifts import ShiftCarWashUpdateCallbackData
from enums import ShiftWorkType
from models import (
    AvailableDate, CarWash,
    ShiftCarsCountByStaff,
    ShiftCarsWithoutWindshieldWasher,
    ShiftFinishResult, ShiftListItem, Staff,
)
from views.base import MediaGroupView, TextView
from views.button_texts import ButtonText

__all__ = (
    'ShiftWorkTypeChoiceView',
    'shift_work_types_and_names',
    'ShiftCarsCountByStaffView',
    'ShiftCarsWithoutWindshieldWasherView',
    'ShiftCarWashUpdateView',
    'ShiftFinishConfirmView',
    'ShiftFinishPhotoConfirmView',
    'ShiftFinishConfirmAllView',
    'ShiftFinishPhotosView',
    'StaffShiftFinishedNotificationView',
    'StaffShiftFinishedView',
    'StaffFirstShiftFinishedView',
    'ShiftStartConfirmView',
    'ShiftStartCarWashChooseView',
    'ShiftApplyChooseMonthView',
    'ShiftApplyScheduleMonthCalendarWebAppView',
    'StaffShiftScheduleCreatedNotificationView',
    'StaffHasNoAnyCreatedShiftView',
    'StaffScheduleCreatedShiftView',
    'ExtraShiftScheduleWebAppView',
    'ExtraShiftScheduleNotificationView',
    'ExtraShiftStartView',
    'ShiftStartRequestView',
    'ShiftImmediateStartRequestView',
)

shift_work_types_and_names: tuple[tuple[ShiftWorkType, str], ...] = (
    (ShiftWorkType.MOVE_TO_WASH, 'Перегон ТС на мойку'),
    (ShiftWorkType.LIGHT_WASHES, 'Легкие мойки'),
    (ShiftWorkType.FIND_VEHICLE_IN_CITY, 'Поиск ТС в городе'),
    (ShiftWorkType.ASSIGNMENT_MOVE, 'Перегон по заданию'),
)


class ShiftWorkTypeChoiceView(TextView):
    text = 'Выберите направление, в котором хотите начать смену:'
    reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=shift_work_type_name,
                    callback_data=ShiftWorkTypeChoiceCallbackData(
                        work_type=shift_work_type,
                    ).pack(),
                )
            ]
            for shift_work_type, shift_work_type_name in
            shift_work_types_and_names
        ]
    )


month_names: Final[tuple[str, ...]] = (
    'январь',
    'февраль',
    'март',
    'апрель',
    'май',
    'июнь',
    'июль',
    'август',
    'сентябрь',
    'октябрь',
    'ноябрь',
    'декабрь',
)


class ShiftCarsCountByStaffView(TextView):

    def __init__(self, shift_cars: ShiftCarsCountByStaff):
        self.__shift_cars = shift_cars

    def get_text(self) -> str:
        lines: list[str] = [
            f'<b>Смена {self.__shift_cars.date:%d.%m.%Y}</b>',
        ]
        if not self.__shift_cars.cars:
            lines.append('Пока нет внесенных авто')
        for position, item in enumerate(
                self.__shift_cars.cars,
                start=1,
        ):
            lines.append(
                f'{position}. {item.staff_full_name} - {item.cars_count} авто'
            )

        return '\n'.join(lines)


class ShiftCarsWithoutWindshieldWasherView(TextView):

    def __init__(self, shift_cars: ShiftCarsWithoutWindshieldWasher):
        self.__shift_cars = shift_cars

    def get_text(self) -> str:
        lines: list[str] = [
            f'<b>Смена {self.__shift_cars.date:%d.%m.%Y}</b>',
        ]
        if not self.__shift_cars.cars:
            lines.append('Пока нет авто с недоливами')
        for car_number in self.__shift_cars.cars:
            lines.append(car_number)

        return '\n'.join(lines)


class ShiftCarWashUpdateView(TextView):
    text = 'Выберите мойку'

    def __init__(self, car_washes: Iterable[CarWash]):
        self.__car_washes = tuple(car_washes)

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardBuilder()
        keyboard.max_width = 1

        for car_wash in self.__car_washes:
            keyboard.button(
                text=car_wash.name,
                callback_data=ShiftCarWashUpdateCallbackData(
                    car_wash_id=car_wash.id,
                ),
            )

        return keyboard.as_markup()


class ShiftFinishConfirmView(TextView):
    text = 'Подтверждаете завершение смены?'
    reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='✅ Да',
                    callback_data=CallbackDataPrefix
                    .SHIFT_FINISH_FLOW_START_ACCEPT,
                ),
                InlineKeyboardButton(
                    text='❌ Нет',
                    callback_data=CallbackDataPrefix
                    .SHIFT_FINISH_FLOW_START_REJECT,
                ),
            ],
        ],
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

    def __init__(
            self,
            *,
            statement_photo_file_id: str,
            service_app_photo_file_id: str,
    ):
        self.__statement_photo_file_id = statement_photo_file_id
        self.__service_app_photo_file_id = service_app_photo_file_id

    def get_medias(self) -> list[MediaType]:
        return [
            InputMediaPhoto(
                media=self.__statement_photo_file_id,
            ),
            InputMediaPhoto(
                media=self.__service_app_photo_file_id,
            ),
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


class ShiftStartConfirmView(TextView):

    def __init__(self, shift_id: int, staff_full_name: str):
        self.__shift_id = shift_id
        self.__staff_full_name = staff_full_name

    def get_text(self) -> str:
        return f'{self.__staff_full_name} подтвердите выход на смену'

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text='✅ Подтвердить',
                        callback_data=ShiftStartCallbackData(
                            shift_id=self.__shift_id,
                        ).pack(),
                    ),
                    InlineKeyboardButton(
                        text='❌ Отклонить',
                        callback_data=ShiftRejectCallbackData(
                            shift_id=self.__shift_id,
                        ).pack(),
                    ),
                ]
            ]
        )


class ShiftStartCarWashChooseView(TextView):
    text = 'Выберите мойку'

    def __init__(self, car_washes: Iterable[CarWash]):
        self.__car_washes = tuple(car_washes)

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardBuilder()
        keyboard.max_width = 1

        for car_wash in self.__car_washes:
            keyboard.button(
                text=car_wash.name,
                callback_data=ShiftStartCarWashCallbackData(
                    car_wash_id=car_wash.id,
                )
            )

        return keyboard.as_markup()


class ShiftApplyChooseMonthView(TextView):

    def __init__(
            self,
            available_dates: Iterable[AvailableDate],
            timezone: ZoneInfo,
    ):
        self.__available_dates = tuple(available_dates)
        self.__timezone = timezone

    def get_text(self) -> str:
        if self.__available_dates:
            return '📆 Выберите месяц'
        return '❌ Нет доступных месяцев для записи на смену'

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardBuilder()
        keyboard.max_width = 1

        now = datetime.datetime.now(self.__timezone)

        for available_date in self.__available_dates:
            month_name = month_names[available_date.month - 1]

            if available_date.year == now.year:
                text = month_name
            else:
                text = f'{month_name} - {available_date.year} год'

            keyboard.button(
                text=text.capitalize(),
                callback_data=ShiftApplyCallbackData(
                    month=available_date.month,
                    year=available_date.year,
                ),
            )

        return keyboard.as_markup()


class ShiftApplyScheduleMonthCalendarWebAppView(TextView):

    def __init__(
            self,
            web_app_base_url: str,
            month: int,
            year: int,
    ):
        self.__web_app_base_url = web_app_base_url
        self.__month = month
        self.__year = year

    def get_text(self) -> str:
        month_name = month_names[self.__month - 1]
        return (
            f'📆 Выберите даты для выхода на смены за {month_name}'
            f' {self.__year} года'
        )

    def get_reply_markup(self) -> ReplyKeyboardMarkup:
        url = (
            f'{self.__web_app_base_url}/shifts/apply'
            f'?year={self.__year}&month={self.__month}'
        )
        return ReplyKeyboardMarkup(
            resize_keyboard=True,
            keyboard=[
                [
                    KeyboardButton(
                        text=ButtonText.SHIFT_SCHEDULE_MONTH_CALENDAR,
                        web_app=WebAppInfo(url=url)
                    ),
                ],
                [
                    KeyboardButton(text=ButtonText.MAIN_MENU),
                ],
            ],
        )


class StaffShiftScheduleCreatedNotificationView(TextView):

    def __init__(self, staff_full_name: str):
        self.__staff_full_name = staff_full_name

    def get_text(self) -> str:
        return f'Сотрудник {self.__staff_full_name} внес график работы'


class StaffHasNoAnyCreatedShiftView(TextView):
    text = '❗️ Вы еще не заполнили график'
    reply_markup = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [
                KeyboardButton(text=ButtonText.SHIFT_APPLY),
            ],
            [
                KeyboardButton(text=ButtonText.MAIN_MENU),
            ],
        ],
    )


class StaffScheduleCreatedShiftView(TextView):

    def __init__(self, shift_dates: Iterable[datetime.date]):
        self.__shift_dates = tuple(shift_dates)

    def get_text(self) -> str:
        lines: list[str] = ['<b>📆 Даты последнего заполненного графика</b>']

        for i, shift_date in enumerate(self.__shift_dates, start=1):
            lines.append(f'{i}. {shift_date:%d.%m.%Y}')

        return '\n'.join(lines)


class ExtraShiftScheduleWebAppView(TextView):
    text = '📆 Выберите дату'

    def __init__(self, web_app_base_url: str):
        self.__web_app_base_url = web_app_base_url

    def get_reply_markup(self) -> ReplyKeyboardMarkup:
        url = f'{self.__web_app_base_url}/shifts/extra'
        return ReplyKeyboardMarkup(
            resize_keyboard=True,
            keyboard=[
                [
                    KeyboardButton(
                        text=ButtonText.EXTRA_SHIFT_CALENDAR,
                        web_app=WebAppInfo(url=url),
                    ),
                ],
                [
                    KeyboardButton(text=ButtonText.MAIN_MENU),
                ],
            ],
        )


class ExtraShiftScheduleNotificationView(TextView):

    def __init__(
            self,
            staff_id: int,
            staff_full_name: str,
            shift_date: datetime.date,
    ):
        self.__staff_id = staff_id
        self.__staff_full_name = staff_full_name
        self.__shift_date = shift_date

    def get_text(self) -> str:
        return (
            f'Сотрудник {self.__staff_full_name} запросил доп.смену'
            f' на дату {self.__shift_date:%d.%m.%Y}'
        )

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        accept_button = InlineKeyboardButton(
            text='✅ Подтвердить',
            callback_data=ExtraShiftCreateAcceptCallbackData(
                staff_id=self.__staff_id,
                date=self.__shift_date,
            ).pack(),
        )
        reject_button = InlineKeyboardButton(
            text='❌ Отклонить',
            callback_data=ExtraShiftCreateRejectCallbackData(
                staff_id=self.__staff_id,
                date=self.__shift_date,
            ).pack(),
        )
        return InlineKeyboardMarkup(
            inline_keyboard=[[accept_button, reject_button]],
        )


class ExtraShiftStartView(TextView):

    def __init__(
            self,
            staff_full_name: str,
            shift_date: datetime.date
    ):
        self.__staff_full_name = staff_full_name
        self.__shift_date = shift_date

    def get_text(self) -> str:
        return (
            f'✅ {self.__staff_full_name}, ваш запрос на доп.смену на дату'
            f' {self.__shift_date:%d.%m.%Y} подтвержден'
        )

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        button = InlineKeyboardButton(
            text='🚀 Начать доп.смену',
            callback_data=ExtraShiftStartCallbackData(
                date=self.__shift_date,
            ).pack(),
        )
        return InlineKeyboardMarkup(inline_keyboard=[[button]])


class ShiftStartRequestView(TextView):

    def __init__(self, *, staff: Staff, shift: ShiftListItem):
        self.__staff = staff
        self.__shift = shift

    def get_text(self) -> str:
        return (
            f'📆 Сотрудник {self.__staff.full_name}'
            f' хочет начать сегодняшнюю смену'
        )

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        accept_button = InlineKeyboardButton(
            text='✅ Подтвердить',
            callback_data=ShiftStartRequestAcceptCallbackData(
                shift_id=self.__shift.id,
            ).pack(),
        )
        reject_button = InlineKeyboardButton(
            text='❌ Отклонить',
            callback_data=ShiftStartRequestRejectCallbackData(
                shift_id=self.__shift.id,
            ).pack(),
        )
        return InlineKeyboardMarkup(
            inline_keyboard=[[accept_button, reject_button]],
        )


class ShiftImmediateStartRequestView(TextView):

    def __init__(self, *, date: datetime.date):
        self.__date = date

    def get_text(self) -> str:
        return f'📆 Начните смену на дату {self.__date:%d.%m.%Y}'

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        button = InlineKeyboardButton(
            text='🚀 Начать смену',
            callback_data=ShiftImmediateStartCallbackData(
                date=self.__date,
            ).pack()
        )
        return InlineKeyboardMarkup(inline_keyboard=[[button]])

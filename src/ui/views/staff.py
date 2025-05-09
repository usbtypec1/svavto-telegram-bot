from aiogram.types import (
    InlineKeyboardButton, InlineKeyboardMarkup,
    WebAppInfo,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from callback_data import (
    StaffDetailCallbackData,
    StaffListCallbackData,
    StaffUpdateCallbackData,
)
from callback_data.prefixes import CallbackDataPrefix
from enums import StaffType, StaffUpdateAction
from models import Staff, StaffDetail, StaffListPage
from ui.buttons import create_back_button
from ui.views.base import TextView


__all__ = ('StaffListView', 'StaffDetailView', 'StaffMenuView')


class StaffMenuView(TextView):
    text = '👥 Cотрудники'
    reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='👥 Все сотрудники',
                    callback_data=StaffListCallbackData(
                        include_banned=True,
                        limit=10,
                        offset=0,
                    ).pack(),
                ),
            ],
            [
                InlineKeyboardButton(
                    text='🌟 Только активные',
                    callback_data=StaffListCallbackData(
                        include_banned=False,
                        limit=10,
                        offset=0,
                    ).pack(),
                ),
            ],
        ],
    )


class StaffListView(TextView):

    def __init__(self, staff_list_page: StaffListPage, include_banned: bool):
        self.__staff_list_page = staff_list_page
        self.__include_banned = include_banned

    def get_text(self) -> str:
        if not self.__staff_list_page.staff:
            return '😔 Нет зарегистрированных сотрудников'
        if self.__include_banned:
            return '👥 Все сотрудники'
        return '👥 Активные сотрудники'

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardBuilder()

        pagination = self.__staff_list_page.pagination

        for staff in self.__staff_list_page.staff:
            callback_data = StaffDetailCallbackData(
                staff_id=staff.id,
                include_banned=self.__include_banned,
                limit=pagination.limit,
                offset=pagination.offset,
            )
            button = InlineKeyboardButton(
                text=staff.full_name,
                callback_data=callback_data.pack()
            )
            keyboard.row(button)

        pagination_buttons_row: list[InlineKeyboardButton] = []

        if not pagination.is_first_page:
            pagination_buttons_row.append(
                InlineKeyboardButton(
                    text=f'← Страница {pagination.previous_page_number}',
                    callback_data=StaffListCallbackData(
                        include_banned=self.__include_banned,
                        limit=pagination.limit,
                        offset=pagination.previous_offset,
                    ).pack(),
                ),
            )

        if not pagination.is_last_page:
            pagination_buttons_row.append(
                InlineKeyboardButton(
                    text=f'Страница {pagination.next_page_number} →',
                    callback_data=StaffListCallbackData(
                        include_banned=self.__include_banned,
                        limit=pagination.limit,
                        offset=pagination.next_offset,
                    ).pack(),
                ),
            )

        if pagination_buttons_row:
            keyboard.row(*pagination_buttons_row)

        keyboard.row(
            create_back_button(
                callback_data=CallbackDataPrefix.STAFF_LIST,
            ),
        )
        return keyboard.as_markup()


class StaffDetailView(TextView):

    def __init__(
            self,
            staff: StaffDetail,
            web_app_base_url: str,
            include_banned: bool,
            limit: int,
            offset: int,
            username: str | None = None,
    ):
        self.__staff = staff
        self.__web_app_base_url = web_app_base_url
        self.__include_banned = include_banned
        self.__limit = limit
        self.__offset = offset
        self.__username = username

    def get_text(self) -> str:
        if self.__staff.is_banned:
            banned_status_line = '<b>❌ Заблокирован</b>\n'
        else:
            banned_status_line = ''

        if self.__username is not None:
            username_line = f'👤 <b>Никнейм:</b> @{self.__username}\n'
        else:
            username_line = ''

        if self.__staff.type == StaffType.CAR_TRANSPORTER:
            staff_type = 'Перегонщик'
        else:
            staff_type = 'Перегонщик-мойщик'

        return (
            f'📱 <b>ID:</b> {self.__staff.id}\n'
            f'👤 <b>ФИО:</b> {self.__staff.full_name}\n'
            f'{username_line}'
            '📞 <b>Номер телефона в каршеринге:</b>'
            f' {self.__staff.car_sharing_phone_number}\n'
            '📞 <b>Номер телефона в Консоли:</b>'
            f' {self.__staff.console_phone_number}\n'
            f'{banned_status_line}'
            f'Специализация: {staff_type}\n'
            f'📅 <b>Дата регистрации:</b>'
            f' {self.__staff.created_at:%d.%m.%Y %H:%M:%S}'
        )

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardBuilder()
        keyboard.max_width = 1

        if self.__staff.type == StaffType.CAR_TRANSPORTER:
            keyboard.button(
                text='Сделать перегонщиком-мойщиком',
                callback_data=StaffUpdateCallbackData(
                    staff_id=self.__staff.id,
                    action=StaffUpdateAction.TO_CAR_TRANSPORTER_AND_WASHER,
                    include_banned=self.__include_banned,
                    limit=self.__limit,
                    offset=self.__offset,
                ),
            )
        else:
            keyboard.button(
                text='Сделать перегонщиком',
                callback_data=StaffUpdateCallbackData(
                    staff_id=self.__staff.id,
                    action=StaffUpdateAction.TO_CAR_TRANSPORTER,
                    include_banned=self.__include_banned,
                    limit=self.__limit,
                    offset=self.__offset,
                ),
            )

        if self.__staff.is_banned:
            keyboard.button(
                text='🔑 Разблокировать',
                callback_data=StaffUpdateCallbackData(
                    staff_id=self.__staff.id,
                    action=StaffUpdateAction.UNBAN,
                    include_banned=self.__include_banned,
                    limit=self.__limit,
                    offset=self.__offset,
                ),
            )
        else:
            keyboard.button(
                text='❌ Заблокировать',
                callback_data=StaffUpdateCallbackData(
                    staff_id=self.__staff.id,
                    action=StaffUpdateAction.BAN,
                    include_banned=self.__include_banned,
                    limit=self.__limit,
                    offset=self.__offset,
                ),
            )
        penalties_url = (f'{self.__web_app_base_url}/penalties/'
                         f'{self.__staff.id}')
        keyboard.button(
            text='🛑 Штрафы',
            web_app=WebAppInfo(url=penalties_url),
        )

        surcharges_url = (
            f'{self.__web_app_base_url}/surcharges/{self.__staff.id}'
        )
        keyboard.button(
            text='💰 Доплаты',
            web_app=WebAppInfo(url=surcharges_url),
        )
        keyboard.row(
            create_back_button(
                callback_data=StaffListCallbackData(
                    include_banned=self.__include_banned,
                    limit=self.__limit,
                    offset=self.__offset,
                ),
            )
        )

        return keyboard.as_markup()

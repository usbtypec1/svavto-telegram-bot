from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ForceReply,
    ReplyKeyboardMarkup,
    KeyboardButton,
    WebAppInfo,
)

from callback_data import MailingTypeChooseCallbackData
from callback_data.prefixes import CallbackDataPrefix
from enums import MailingType
from views.base import TextView
from views.button_texts import ButtonText

__all__ = (
    'MailingTypeChooseView',
    'MailingTextInputView',
    'MailingReplyMarkupWebAppView',
    'MailingConfirmView',
    'MailingStaffWebAppView',
)


class MailingTypeChooseView(TextView):
    text = 'Выберите тип рассылки'
    reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Всем',
                    callback_data=MailingTypeChooseCallbackData(
                        type=MailingType.ALL,
                    ).pack(),
                ),
            ],
            [
                InlineKeyboardButton(
                    text='Конкретным пользователям',
                    callback_data=MailingTypeChooseCallbackData(
                        type=MailingType.SPECIFIC_STAFF,
                    ).pack(),
                ),
            ],
            [
                InlineKeyboardButton(
                    text='Активным за последние 30 дн.',
                    callback_data=MailingTypeChooseCallbackData(
                        type=MailingType.LAST_ACTIVE,
                    ).pack(),
                ),
            ],
        ],
    )


class MailingTextInputView(TextView):
    text = 'Введите текст рассылки (вы можете использовать форматирование)'
    reply_markup = ForceReply(input_field_placeholder='Текст рассылки')


class MailingReplyMarkupWebAppView(TextView):
    text = 'Хотите ли привязать кнопки в тексту рассылки?'

    def __init__(self, web_app_base_url: str):
        self.__web_app_base_url = web_app_base_url

    def get_reply_markup(self) -> ReplyKeyboardMarkup:
        web_app_button = KeyboardButton(
            text=ButtonText.ATTACH_REPLY_MARKUP,
            web_app=WebAppInfo(
                url=f'{self.__web_app_base_url}/mailing/reply-markup',
            ),
        )
        main_menu_button = KeyboardButton(text=ButtonText.MAIN_MENU)
        skip_button = KeyboardButton(text=ButtonText.SKIP)
        return ReplyKeyboardMarkup(
            resize_keyboard=True,
            keyboard=[
                [web_app_button],
                [skip_button],
                [main_menu_button],
            ],
        )


class MailingStaffWebAppView(TextView):
    text = 'Выберите сотрудников'

    def __init__(self, web_app_base_url: str):
        self.__web_app_base_url = web_app_base_url

    def get_reply_markup(self) -> ReplyKeyboardMarkup:
        web_app_button = KeyboardButton(
            text=ButtonText.MAILING_STAFF,
            web_app=WebAppInfo(
                url=f'{self.__web_app_base_url}/mailing/staff',
            ),
        )
        return ReplyKeyboardMarkup(
            resize_keyboard=True,
            keyboard=[[web_app_button]],
        )


class MailingConfirmView(TextView):
    text = 'Вы уверены что хотите отправить рассылку?'
    reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Отправить',
                    callback_data=CallbackDataPrefix.MAILING_CREATE_ACCEPT,
                ),
                InlineKeyboardButton(
                    text='Отклонить',
                    callback_data=CallbackDataPrefix.MAILING_CREATE_REJECT,
                )
            ]
        ]
    )

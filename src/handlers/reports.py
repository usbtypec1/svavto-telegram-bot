from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery, Message

from callback_data.prefixes import CallbackDataPrefix
from config import Config
from filters import admins_filter

__all__ = ('router',)

from views.admins import AdminOtherMenuView
from views.base import answer_view

from views.button_texts import ButtonText

router = Router(name=__name__)


@router.message(
    F.text == ButtonText.OTHER,
    admins_filter,
    StateFilter('*'),
)
async def on_other(
        message: Message,
        config: Config,
) -> None:
    view = AdminOtherMenuView(config.web_app_base_url)
    await answer_view(message, view)


@router.callback_query(
    F.data == CallbackDataPrefix.REPORTS,
    admins_filter,
    StateFilter('*'),
)
async def on_show_reports(callback_query: CallbackQuery) -> None:
    await callback_query.message.answer(
        '📊 Таблица 1: <a href="https://docs.google.com/spreadsheets/d'
        '/1q6eSsP3JtPe3J517vf_KEsZWiIiFYMc9h7h_CMFiaG4/edit?gid=0#gid=0'
        '">*ссылка*</a>'
        '\n📊 Таблица 2: <a href="https://docs.google.com/spreadsheets/d'
        '/1q6eSsP3JtPe3J517vf_KEsZWiIiFYMc9h7h_CMFiaG4/edit?gid=0#gid=0'
        '">*ссылка*</a>'
    )
    await callback_query.answer()

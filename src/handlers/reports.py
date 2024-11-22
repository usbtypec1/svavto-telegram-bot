from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.types import Message

from config import Config
from filters import admins_filter
from views.admins import AdminOtherMenuView
from views.base import answer_view
from views.button_texts import ButtonText

__all__ = ('router',)

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


@router.message(
    F.text == ButtonText.REPORTS,
    admins_filter,
    StateFilter('*'),
)
async def on_show_reports(message: Message) -> None:
    await message.answer(
        '📊 Услуги: <a href="https://docs.google.com/spreadsheets/d/'
        '1lV77O1DquJqdC_zqXD0aRkp1C4IRKQjMlQMjnS4K8Fc/edit?gid=0#gid=0">'
        '*ссылка*</a>'
    )

from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.types import Message

from config import Config
from filters import admins_filter
from ui.views import AdminOtherMenuView
from ui.views import answer_text_view
from ui.views import ButtonText
from ui.views import ReportTablesView

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
    await answer_text_view(message, view)


@router.message(
    F.text == ButtonText.REPORTS,
    admins_filter,
    StateFilter('*'),
)
async def on_show_reports(message: Message, config: Config) -> None:
    view = ReportTablesView(config.report_tables)
    await answer_text_view(message, view)

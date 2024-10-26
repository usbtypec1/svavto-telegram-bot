from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import Message

__all__ = ('router',)

router = Router(name=__name__)


# @router.message(
#     F.web_app_data,
#     StateFilter('*'),
# )
# async def on_choose_specific_staff(message: Message) -> None:
#     print(message.web_app_data.button_text)
#     await message.reply(message.web_app_data.data)

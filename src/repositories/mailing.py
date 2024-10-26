from collections.abc import Iterable
from typing import TypeAlias

from connections import MailingConnection
from models import Button
from repositories.errors import handle_errors

__all__ = ('MailingRepository',)

ButtonsRows: TypeAlias = Iterable[Iterable[Button]]


class MailingRepository:

    def __init__(self, connection: MailingConnection):
        self.__connection = connection

    async def send_to_all_staff(
            self,
            *,
            text: str,
            reply_markup: ButtonsRows | None,
    ) -> None:
        response = await self.__connection.send_to_all(
            text=text,
            reply_markup=reply_markup
        )
        handle_errors(response)

    async def send_to_specific_staff(
            self,
            *,
            text: str,
            reply_markup: ButtonsRows | None,
            chat_ids: Iterable[int],
    ) -> None:
        response = await self.__connection.send_to_specific_staff(
            text=text,
            reply_markup=reply_markup,
            chat_ids=chat_ids,
        )
        handle_errors(response)

    async def send_to_last_active_staff(
            self,
            *,
            text: str,
            reply_markup: ButtonsRows | None,
            last_days: int,
    ) -> None:
        response = await self.__connection.send_to_last_active_staff(
            text=text,
            reply_markup=reply_markup,
            last_days=last_days,
        )
        handle_errors(response)

import json
from typing import Annotated

from aiogram.types import InlineKeyboardMarkup
from pydantic import BaseModel, Field, constr, field_validator

from enums import MailingType

__all__ = ("MailingParams",)


class MailingParams(BaseModel):
    text: constr(min_length=1, max_length=4096)
    type: MailingType
    photo_file_ids: Annotated[list[str], Field(default_factory=list)]
    chat_ids: Annotated[list[int], Field(default_factory=list)]
    reply_markup: InlineKeyboardMarkup | None = None

    # noinspection PyNestedDecorators
    @field_validator("reply_markup", mode="before")
    @classmethod
    def validate_reply_markup(cls, value):
        if isinstance(value, str):
            return json.loads(value)
        elif value is None:
            return value
        return value

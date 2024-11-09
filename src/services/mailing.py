from collections.abc import Iterable, Sequence
from datetime import UTC, datetime

from aiogram.types import InlineKeyboardMarkup, InputMediaPhoto, Message
from aiogram.utils.media_group import MediaGroupBuilder

from models import Staff

__all__ = (
    'render_message_for_mailing',
    'filter_banned_staff',
    'filter_staff_by_chat_ids',
    'filter_last_active_staff',
)


def filter_staff_by_chat_ids(
        *,
        staff_list: Iterable[Staff],
        chat_ids: Iterable[int],
) -> list[Staff]:
    chat_ids = set(chat_ids)
    return [staff for staff in staff_list if staff.id in chat_ids]


def filter_banned_staff(
        staff_list: Iterable[Staff],
) -> list[Staff]:
    return [staff for staff in staff_list if not staff.is_banned]


def filter_last_active_staff(
        staff_list: Iterable[Staff],
        last_activity_days: int,
) -> list[Staff]:
    result: list[Staff] = []
    now = datetime.now(UTC)
    for staff in staff_list:
        time_since_last_activity = now - staff.last_activity_at
        if time_since_last_activity.days < last_activity_days:
            result.append(staff)
    return result


async def render_message_for_mailing(
        *,
        message: Message,
        text: str,
        photo_file_ids: Sequence[str],
        reply_markup: InlineKeyboardMarkup | None,
) -> None:
    if len(photo_file_ids) == 0:
        await message.answer(text, reply_markup=reply_markup)
    elif len(photo_file_ids) == 1:
        await message.answer_photo(
            photo_file_ids[0],
            text,
            reply_markup=reply_markup,
        )
    else:
        media = [
            InputMediaPhoto(media=photo_file_id)
            for photo_file_id in photo_file_ids
        ]
        builder = MediaGroupBuilder(caption=text, media=media)
        await message.answer_media_group(builder.build())

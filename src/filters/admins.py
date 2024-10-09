from aiogram.types import Message, CallbackQuery

__all__ = ('admins_filter',)


def admins_filter(
        message_or_callback_query: Message | CallbackQuery,
        admin_user_ids: set[int],
) -> bool:
    return message_or_callback_query.from_user.id in admin_user_ids

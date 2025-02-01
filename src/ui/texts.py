from typing import Final

__all__ = (
    'CONFIRM',
    'REJECT',
    'ACCEPT',
    'ACCEPTED',
    'REJECTED',
    'CONFIRMED',
    'format_confirm_text',
    'format_reject_text',
    'format_accept_text',
    'NO_ANY_STAFF',
    'BACK',
)

ACCEPT: Final[str] = '✅ Принять'
ACCEPTED: Final[str] = '✅ Принято'
CONFIRM: Final[str] = '✅ Подтвердить'
REJECT: Final[str] = '❌ Отклонить'
CONFIRMED: Final[str] = '✅ Подтверждено'
REJECTED: Final[str] = '❌ Отклонено'
NO_ANY_STAFF: Final[str] = '😔 Нет сотрудников'
BACK: Final[str] = '🔙 Назад'


def format_accept_text(existing_text: str) -> str:
    return f'{existing_text}\n\n<i>{ACCEPTED}</i>'


def format_confirm_text(existing_text: str) -> str:
    return f'{existing_text}\n\n<i>{CONFIRMED}</i>'


def format_reject_text(existing_text: str) -> str:
    return f'{existing_text}\n\n<i>{REJECTED}</i>'

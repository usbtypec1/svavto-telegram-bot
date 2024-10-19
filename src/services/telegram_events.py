from aiogram.types import ErrorEvent

__all__ = ('answer_appropriate_event',)


async def answer_appropriate_event(event: ErrorEvent, text: str) -> None:
    if event.update.message is not None:
        await event.update.message.answer(text)
    elif event.update.callback_query is not None:
        await event.update.callback_query.answer(text=text, show_alert=True)
    else:
        raise ValueError(f'Invalid event update type: {event.update}')

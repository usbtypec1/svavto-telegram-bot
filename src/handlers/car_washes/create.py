from mailbox import Message

from aiogram import Router

from aiogram.filters import StateFilter

from filters import admins_filter

__all__ = ('router',)

router = Router(name='create-car-wash')


@router.message(
    admins_filter,
    StateFilter('*'),
)
async def on_start_car_wash_create_flow(
        message: Message,

):

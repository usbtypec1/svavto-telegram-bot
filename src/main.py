import asyncio
from collections.abc import Iterable

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (
    BotCommand, BotCommandScope,
    BotCommandScopeAllPrivateChats, BotCommandScopeChat,
)
from fast_depends import Depends, inject

import handlers
from config import Config, load_config_from_file
from logger import setup_logging
from middlewares import banned_staff_middleware
from services.notifications import (
    MailingService, NotificationService,
    SpecificChatsNotificationService,
)


def include_handlers(dispatcher: Dispatcher) -> None:
    dispatcher.include_routers(
        handlers.errors.router,
        handlers.car_washes.router,
        handlers.users.router,
        handlers.shifts.router,
        handlers.staff.router,
        handlers.schedules.router,
        handlers.penalties.router,
        handlers.surcharges.router,
        handlers.mailing.router,
        handlers.cars.router,
        handlers.reports.router,
    )


async def setup_commands(bot: Bot, admin_chat_ids: Iterable[int]) -> None:
    await bot.set_my_commands(
        commands=[
            BotCommand(
                command='start',
                description='Главное меню/меню смены',
            ),
        ],
        scope=BotCommandScopeAllPrivateChats(),
    )

    for chat_id in admin_chat_ids:
        await bot.set_my_commands(
            commands=[
                BotCommand(
                    command='start',
                    description='Меню старшего смены',
                ),
            ],
            scope=BotCommandScopeChat(chat_id=chat_id)
        )


@inject
async def main(
        config: Config = Depends(load_config_from_file),
) -> None:
    setup_logging()
    bot = Bot(
        token=config.telegram_bot_token,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML,
        ),
    )

    admins_notification_service = SpecificChatsNotificationService(
        bot=bot,
        chat_ids=config.admin_user_ids,
    )
    main_chat_notification_service = SpecificChatsNotificationService(
        bot=bot,
        chat_ids=(config.main_chat_id,),
    )

    storage = MemoryStorage()
    dispatcher = Dispatcher(storage=storage)

    dispatcher.update.middleware(banned_staff_middleware)

    dispatcher['config'] = config
    dispatcher['admin_user_ids'] = config.admin_user_ids
    dispatcher['admins_notification_service'] = admins_notification_service
    dispatcher['main_chat_notification_service'] = (
        main_chat_notification_service
    )

    notification_service = NotificationService(bot)
    dispatcher['notification_service'] = notification_service

    mailing_service = MailingService(bot)
    dispatcher['mailing_service'] = mailing_service

    include_handlers(dispatcher)

    await setup_commands(bot, config.admin_user_ids)

    await dispatcher.start_polling(bot)


if __name__ == '__main__':
    # noinspection PyArgumentList
    asyncio.run(main())

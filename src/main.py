import asyncio
from collections.abc import Iterable

import redis.asyncio as redis
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (
    BotCommand, BotCommandScopeAllPrivateChats, BotCommandScopeChat,
)
from fast_depends import Depends, inject
import sentry_sdk

import handlers
from config import Config, load_config_from_file
from dependencies.repositories import get_staff_repository
from logger import setup_logging
from middlewares import banned_staff_middleware
from middlewares.admins import AdminUserIdsMiddleware
from repositories import StaffRepository
from services.notifications import (
    MailingService, NotificationService,
    SpecificChatsNotificationService,
)


def include_handlers(dispatcher: Dispatcher) -> None:
    dispatcher.include_routers(
        handlers.users.router,
        handlers.errors.router,
        handlers.validators_errors.router,
        handlers.car_washes.router,
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
        config: Config = Depends(
            dependency=load_config_from_file,
            use_cache=False,
        ),
        staff_repository: StaffRepository = Depends(
            dependency=get_staff_repository,
            use_cache=False,
        ),
) -> None:
    setup_logging()
    bot = Bot(
        token=config.telegram_bot_token,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML,
        ),
    )

    if config.sentry.is_enabled:
        sentry_sdk.init(
            dsn=config.sentry.dsn,
            traces_sample_rate=config.sentry.traces_sample_rate,
        )

    admin_user_ids = await staff_repository.get_all_admin_user_ids()

    main_chat_notification_service = SpecificChatsNotificationService(
        bot=bot,
        chat_ids=(config.main_chat_id,),
    )

    storage = MemoryStorage()
    dispatcher = Dispatcher(storage=storage)

    admin_user_ids_middleware = AdminUserIdsMiddleware(
        ttl_in_seconds=config.admin_user_ids_ttl_in_seconds,
    )

    redis_client = redis.from_url(config.redis_url, decode_responses=True)
    await redis_client.ping()

    dispatcher.update.outer_middleware(admin_user_ids_middleware)
    dispatcher.update.middleware(banned_staff_middleware)

    dispatcher['config'] = config
    dispatcher['main_chat_notification_service'] = (
        main_chat_notification_service
    )

    dispatcher['redis'] = redis_client

    notification_service = NotificationService(bot)
    dispatcher['notification_service'] = notification_service

    mailing_service = MailingService(bot)
    dispatcher['mailing_service'] = mailing_service

    include_handlers(dispatcher)

    await setup_commands(bot, admin_user_ids)

    await dispatcher.start_polling(bot)


if __name__ == '__main__':
    # noinspection PyArgumentList
    asyncio.run(main())

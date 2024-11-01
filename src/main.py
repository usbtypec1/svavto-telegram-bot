import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from fast_depends import inject, Depends

import handlers
from config import load_config_from_file, Config
from logger import setup_logging
from services import NotificationService
from services.notifications import SpecificChatsNotificationService


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
    dispatcher['config'] = config
    dispatcher['admin_user_ids'] = config.admin_user_ids
    dispatcher['admins_notification_service'] = admins_notification_service
    dispatcher['main_chat_notification_service'] = (
        main_chat_notification_service
    )

    notification_service = NotificationService(bot)
    dispatcher['notification_service'] = notification_service

    include_handlers(dispatcher)

    await dispatcher.start_polling(bot)


if __name__ == '__main__':
    # noinspection PyArgumentList
    asyncio.run(main())

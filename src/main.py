import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import load_config_from_env_vars


async def main() -> None:
    config = load_config_from_env_vars()
    bot = Bot(
        token=config.telegram_bot_token,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML,
        ),
    )
    dispatcher = Dispatcher()

    await dispatcher.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())

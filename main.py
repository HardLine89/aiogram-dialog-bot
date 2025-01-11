import asyncio
import logging
from aiogram import Dispatcher

from bot.handlers.start import start_router
from settings.config import AppConfig

config = AppConfig()


async def main():
    logging.info("Starting bot")
    dp = Dispatcher()

    dp.include_router(start_router)

    await dp.start_polling(config.bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        import platform

        if platform.system() == "Windows":
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Bot stopped")

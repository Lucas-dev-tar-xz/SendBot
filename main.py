import asyncio

import sys

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, FSInputFile
from aiogram.client.default import DefaultBotProperties

import os
from dotenv import load_dotenv

from database.db import mdb

import logging


load_dotenv()

bot = Bot(os.getenv("BOT_TOKEN"), default=DefaultBotProperties(parse_mode="HTML"))

dp = Dispatcher()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
    datefmt="%H:%M:%S",
)

logger = logging.getLogger('main')


async def main():
    logger.info("=" * 60)
    # ========== Routers ==========
    logger.info("Подключаю Routers")

    from handlers.user import router as user_router
    dp.include_routers(user_router)

    # ========== Database ==========
    logger.info("Подключаюсь к Database")

    mdb.create_tables()
    # ========== Pooling ==========
    await dp.start_polling(bot)

    logger.info("Запущено")


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Остановлено пользователем")
        sys.exit(0)
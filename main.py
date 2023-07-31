import asyncio

import betterlogging as logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.utils.chat_action import ChatActionMiddleware
from redis.asyncio.client import Redis
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio.session import async_sessionmaker

from bot.config import load_config
from bot.filters.admin import AdminFilter
from bot.filters.command import CommandFilter
from bot.filters.fuck import FuckFilter
from bot.filters.reply import ReplyFilter
from bot.filters.user import UserFilter
from bot.handlers.ban_handler import ban_user
from bot.handlers.cenz_handler import check_messages
from bot.handlers.hastebin_handler import create_note
from bot.handlers.rating_handler import check_rating, rating_decrease, rating_increase
from bot.handlers.report_handler import report_message
from bot.handlers.ro_handler import read_only_for_user
from bot.middlewares.groups import OnlyGroupsMiddleware
from bot.models import Base
from bot.services.hastebin import HastebinAPI

logger = logging.getLogger(__name__)


async def main() -> None:
    logging.basic_colorized_config(level=logging.INFO)

    config = load_config()
    storage = RedisStorage(redis=Redis(host=config.storage.redis_host,
                                       port=config.storage.redis_port,
                                       db=config.storage.redis_db,
                                       password=config.storage.redis_password),
                           data_ttl=3600)

    bot = Bot(token=config.bot.token, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=storage)
    hastebin = HastebinAPI(config.hastebin.api_key)

    # region Database
    postgres_url = URL.create(
        drivername="postgresql+asyncpg",
        username=config.database.username,
        password=config.database.password,
        host=config.database.host,
        database=config.database.name,
        port=config.database.port,
    )
    async_engine = create_async_engine(postgres_url)
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    session_maker = async_sessionmaker(async_engine)
    # endregion Database

    # Register middlewares and handlers
    dp.message.middleware.register(ChatActionMiddleware())
    dp.message.middleware.register(OnlyGroupsMiddleware())

    dp.message.register(ban_user, CommandFilter('ban'), ReplyFilter(), UserFilter(), AdminFilter())
    dp.message.register(read_only_for_user, CommandFilter('ro'), ReplyFilter(), UserFilter(), AdminFilter())
    dp.message.register(rating_decrease, CommandFilter("dec"), ReplyFilter(), UserFilter(), AdminFilter())
    dp.message.register(report_message, CommandFilter("report"), ReplyFilter(), UserFilter())
    dp.message.register(create_note, CommandFilter('note'), ReplyFilter())
    dp.message.register(check_rating, CommandFilter("rating"))
    dp.message.register(check_messages, FuckFilter())
    dp.message.register(rating_increase, ReplyFilter(), UserFilter())

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot, session_maker=session_maker, hastebin=hastebin)

    finally:
        await dp.storage.close()
        await bot.session.close()
        await async_engine.dispose()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")

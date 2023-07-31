from aiogram.types import Message
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from bot.models import Channel


async def check_user_rating(
    message: Message,
    session_maker: async_sessionmaker[AsyncSession],
) -> int:
    user_id = message.from_user.id
    chat_id = message.chat.id

    async with session_maker() as session:
        async with session.begin():
            select_query = select(Channel).where(
                Channel.user_id == user_id,
                Channel.chat_id == chat_id,
            )
            result_proxy = await session.execute(select_query)
            existing_channel = result_proxy.scalars().first()

            return 0 if existing_channel is None else existing_channel.user_rating

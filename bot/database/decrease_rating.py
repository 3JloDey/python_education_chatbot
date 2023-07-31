from aiogram.types import Message
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from bot.models import Channel


async def decrease_user_rating(
    message: Message,
    session_maker: async_sessionmaker[AsyncSession],
    quantity: int,
) -> int:
    user_id = message.reply_to_message.from_user.id
    chat_id = message.chat.id

    async with session_maker() as session:
        async with session.begin():
            select_query = select(Channel).where(
                Channel.user_id == user_id,
                Channel.chat_id == chat_id,
            )
            result_proxy = await session.execute(select_query)
            existing_channel = result_proxy.scalars().first()
            if existing_channel is not None:
                if existing_channel.user_rating - quantity < 0:
                    existing_channel.user_rating = 0
                else:
                    existing_channel.user_rating -= quantity

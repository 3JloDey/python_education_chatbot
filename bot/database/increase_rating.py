from aiogram.types import Message
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from bot.models import Channel, User
from bot.utils.get_channel import get_channel
from bot.utils.get_user import get_detail_informations, get_user


async def increase_user_rating(
    message: Message,
    session_maker: async_sessionmaker[AsyncSession],
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

            if existing_channel is None:
                user: User = get_user(message)
                channel: Channel = get_channel(message)

                user.channels.append(channel)
                session.add(user)
            else:
                update_query = update(User).where(User.user_id == user_id).values(get_detail_informations(message))
                await session.execute(update_query)

                existing_channel.user_rating += 1

            return 1 if existing_channel is None else existing_channel.user_rating

from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from bot.database.check_rating import check_user_rating
from bot.database.decrease_rating import decrease_user_rating
from bot.database.increase_rating import increase_user_rating
from bot.utils.autodelete_message import delete_message
from bot.utils.gratitude import gratitude_checker


async def rating_increase(
    message: Message,
    session_maker: async_sessionmaker[AsyncSession],
) -> None:
    if gratitude_checker(message.text):
        from_user_id = message.from_user.id
        from_user_name = message.from_user.full_name
        from_user = f'<a href="tg://user?id={from_user_id}">{from_user_name}</a>'

        to_user_id = message.reply_to_message.from_user.id
        to_user_name = message.reply_to_message.from_user.full_name
        to_user = f'<a href="tg://user?id={to_user_id}">{to_user_name}</a>'

        reputation = await increase_user_rating(message, session_maker)
        msg = await message.answer(
            f"{to_user}, пользователь {from_user} повысил вам репутацию!\n"
            f"<i>Текущий рейтинг: {reputation}</i>"
        )
        await delete_message(msg, 120)


async def rating_decrease(
    message: Message,
    session_maker: async_sessionmaker[AsyncSession],
) -> None:
    await message.delete()
    command = message.text.split()
    if len(command) > 1 and command[-1].isdigit():
        quantity = int(command[-1])
        await decrease_user_rating(message, session_maker, quantity)


async def check_rating(
    message: Message,
    session_maker: async_sessionmaker[AsyncSession],
) -> None:
    user_id = message.from_user.id
    user_name = message.from_user.full_name
    user = f'<a href="tg://user?id={user_id}">{user_name}</a>'

    reputation = await check_user_rating(message, session_maker)
    msg = await message.reply(f"<i>{user}, ваш рейтинг: {reputation}</i>")
    await delete_message([message, msg], 5)

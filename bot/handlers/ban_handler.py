from datetime import timedelta

from aiogram import Bot
from aiogram.types import Message


async def ban_user(message: Message, bot: Bot) -> None:
    await message.delete()

    if message.text.split()[-1].isdigit():
        user = message.reply_to_message.from_user
        ban_time = int(message.text.split()[-1])
        link = f'<a href="tg://user?id={user.id}">{user.full_name}</a>'

        await bot.ban_chat_member(
            chat_id=message.chat.id,
            user_id=user.id,
            until_date=timedelta(days=ban_time),
        )

        await message.answer(f"Пользователь {link} был заблокирован на {ban_time} дней.")

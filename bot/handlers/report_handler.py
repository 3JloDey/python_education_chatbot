from contextlib import suppress

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message


async def report_message(message: Message, bot: Bot):
    await message.delete()
    admins = await bot.get_chat_administrators(message.chat.id)
    reply_message = message.reply_to_message

    message_link = reply_message.get_url()
    user_link = f'<a href="tg://user?id={message.from_user.id}">{message.from_user.full_name}</a>'
    author = f'<a href="tg://user?id={reply_message.from_user.id}">{reply_message.from_user.full_name}</a>'

    text = f"{user_link} отправил репорт.\nАвтор сообщения: {author}\nСсылка: {message_link}\nКопия сообщения 👇🏻"

    for admin in admins:
        if not admin.user.is_bot:
            with suppress(TelegramBadRequest):
                await bot.send_message(chat_id=admin.user.id, text=text)
                await bot.copy_message(
                    chat_id=admin.user.id,
                    from_chat_id=message.chat.id,
                    message_id=reply_message.message_id,
                )

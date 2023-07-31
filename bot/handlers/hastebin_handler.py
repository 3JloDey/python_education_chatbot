from aiogram.types import Message

from bot.services.hastebin import HastebinAPI


async def create_note(message: Message, hastebin: HastebinAPI) -> None:
    await message.delete()

    url = await hastebin.create_document(message.reply_to_message.text)

    if url is not None:
        user_full_name = message.reply_to_message.from_user.full_name

        text = f'<a href="{url}">✅ Hastebin-блокнот пользователя {user_full_name}</a>'
        await message.answer(text=text, disable_notification=True)
    else:
        text = "⚠️ При создании ссылки возникла ошибка, попробуйте позже."
        await message.answer(text=text, disable_notification=True)

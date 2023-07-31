from datetime import timedelta

from aiogram import Bot
from aiogram.types import Message
from aiogram.types.chat_permissions import ChatPermissions


async def read_only_for_user(message: Message, bot: Bot) -> None:
    await message.delete()

    if message.text.split()[-1].isdigit():
        user = message.reply_to_message.from_user
        ro_time = int(message.text.split()[-1])
        link = f'<a href="tg://user?id={user.id}">{user.full_name}</a>'

        permissions = ChatPermissions(
            can_send_messages=False,
            can_send_other_messages=False,
            can_send_documents=False,
            can_send_photos=False,
            can_send_videos=False,
            can_send_audios=False,
            can_send_video_notes=False,
            can_send_voice_notes=False,
            can_send_polls=False,
        )
        await bot.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=user.id,
            permissions=permissions,
            until_date=timedelta(minutes=ro_time),
        )
        await message.answer(f"Пользователю {link} включен режим ReadOnly на {ro_time} минут.")

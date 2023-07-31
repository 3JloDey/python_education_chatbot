from aiogram import Bot
from aiogram.enums.chat_member_status import ChatMemberStatus
from aiogram.filters import Filter
from aiogram.types import Message


class AdminFilter(Filter):
    async def __call__(self, message: Message, bot: Bot) -> bool:
        from_user = await bot.get_chat_member(
            chat_id=message.chat.id,
            user_id=message.from_user.id,
        )
        to_user = await bot.get_chat_member(
            chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id
        )

        admin_status = (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR)
        if from_user.status in admin_status and to_user not in admin_status:
            return True

from string import punctuation

from aiogram import Bot
from aiogram.enums.chat_member_status import ChatMemberStatus
from aiogram.filters import Filter
from aiogram.types import Message

from bot.utils.get_cenz_words import get_cenz_data


class FuckFilter(Filter):
    def __init__(self) -> None:
        self.cenz = get_cenz_data()

    async def __call__(self, message: Message, bot: Bot) -> bool:
        chat_member = await bot.get_chat_member(
            chat_id=message.chat.id,
            user_id=message.from_user.id,
        )
        if chat_member.status in (
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.CREATOR,
        ):
            return False

        cleaned_text = {
            word.translate(str.maketrans("", "", punctuation))
            for word in message.text.lower().split()
        }
        if cleaned_text.intersection(self.cenz):
            return True
        return False

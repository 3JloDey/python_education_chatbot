from aiogram.types import Message
from bot.models import Channel


def get_channel(message: Message) -> Channel:
    return Channel(
        chat_id=message.chat.id,
        type=message.chat.type,
        full_name=message.chat.full_name,
        user_rating=1,
    )

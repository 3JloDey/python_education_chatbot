from aiogram.filters import Filter
from aiogram.types import Message


class UserFilter(Filter):
    async def __call__(self, message: Message) -> bool:
        return (
            not message.reply_to_message.from_user.is_bot
            and message.reply_to_message.from_user.id != message.from_user.id
        )

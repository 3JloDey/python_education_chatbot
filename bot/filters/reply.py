from aiogram.filters import Filter
from aiogram.types import Message


class ReplyFilter(Filter):
    async def __call__(self, message: Message) -> bool:
        return message.reply_to_message is not None

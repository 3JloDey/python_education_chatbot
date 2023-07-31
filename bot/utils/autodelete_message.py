import asyncio
from contextlib import suppress

from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message


async def delete_message(message: Message | list[Message], time: int = 0):
    with suppress(TelegramBadRequest):
        await asyncio.sleep(time)

        if isinstance(message, Message):
            await message.delete()

        elif isinstance(message, list):
            for msg in message:
                await msg.delete()

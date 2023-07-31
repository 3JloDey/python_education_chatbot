from aiogram.types import Message

from bot.models import User


def get_user(message: Message | None) -> User | None:
    if message is None or message.reply_to_message is None:
        return None
    user = message.reply_to_message.from_user

    return User(
        user_id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        full_name=user.full_name,
        username=user.username,
        is_premium=user.is_premium,
    )


def get_detail_informations(message: Message | None) -> dict | None:
    if message is None or message.reply_to_message is None:
        return None
    user = message.reply_to_message.from_user

    return dict(
        first_name=user.first_name,
        last_name=user.last_name,
        full_name=user.full_name,
        username=user.username,
        is_premium=user.is_premium,
    )

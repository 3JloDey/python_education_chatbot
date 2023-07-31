from datetime import timedelta

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.types.chat_permissions import ChatPermissions

from bot.utils.autodelete_message import delete_message


async def check_messages(message: Message, bot: Bot, state: FSMContext) -> None:
    await message.delete()

    user_id = str(message.from_user.id)
    user_full_name = message.from_user.full_name

    data = await state.get_data()
    permissions = ChatPermissions(
        can_send_messages=False,
        can_send_other_messages=False,
        can_send_documents=False,
        can_send_audios=False,
        can_send_photos=False,
        can_send_video_notes=False,
        can_send_voice_notes=False,
        can_send_polls=False,
        can_send_videos=False,
        can_pin_messages=False,
    )

    if user_id in data:
        data[user_id] += 1
        if data[user_id] > 2:
            await bot.restrict_chat_member(
                chat_id=message.chat.id,
                user_id=int(user_id),
                permissions=permissions,
                until_date=timedelta(hours=1, minutes=1),
            )
    else:
        data[user_id] = 1

    user = f'<a href="tg://user?id={user_id}">{user_full_name}</a>'
    msg = await message.answer(
        f"{user}, в вашем предложении обнаружен мат!\n"
        "Дальнейшее использование нецензурной лексики приведёт к блокировке.\n"
        f"<u>Кол-во предупреждений: {data[user_id]}/{3 if data[user_id] <= 3 else data[user_id]}</u>"
    )
    await state.update_data(data)
    await delete_message(msg, 20)

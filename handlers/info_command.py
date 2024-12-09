from aiogram import Router , types
from aiogram.filters import Command

command_router = Router()


@command_router.message(Command("myinfo"))
async def myinfo_command(message: types.Message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    username = message.from_user.username or "Не указан"

    response = (
        f"🔎 **Ваши данные:**\n\n"
        f"🆔 **ID:** {user_id}\n"
        f"👤 **Имя:** {first_name}\n"
        f"📛 **Username:** {username}"
    )

    await message.reply(response, parse_mode="Markdown")
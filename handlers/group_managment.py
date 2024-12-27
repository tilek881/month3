from aiogram import types, Router , F
from datetime import datetime, timedelta
import re

group_router = Router()
group_router.message.filter(F.chat.type != "private")

BANNED_WORDS = ["дурак", "дебил" , "дегроид" , "урод" , "сброд" , "чурбан"]

@group_router.message(F.text)
async def check_banned_words(message: types.Message):
    if any(word in message.text.lower() for word in BANNED_WORDS):
        user_to_ban = message.from_user
        await message.chat.ban(user_id=user_to_ban.id)
        await message.reply(f"Пользователь @{user_to_ban.id} забанен за использование запрещенных слов.")
        return


@group_router.message(F.text.lower().startswith("бан"))
async def ban_user(message: types.Message):
    if not message.reply_to_message:
        await message.reply("бан должен быть ответом на сообщение пользователя, которого вы хотите забанить.")
        return

    match = re.search(r"\d+[дчнм]", message.text.lower())
    if not match:
        await message.reply("Укажите временной период в формате, например: '1д', '4ч', '20м' , '20м' .")
        return

    time_str = match.group()
    unit = time_str[-1]
    value = int(time_str[:-1])

    if unit == "д":
        delta = timedelta(days=value)
    elif unit == "ч":
        delta = timedelta(hours=value)
    elif unit == "н":
        delta = timedelta(weeks=value)
    elif unit == "м":
        delta = timedelta(minutes=value)
    else:
        await message.reply("Неверный формат времени. Используйте 'д' для дней, 'ч' для часов, 'н' для недель, 'м' для минут.")
        return

    user_to_ban = message.reply_to_message.from_user
    until_date = datetime.now() + delta
    await message.chat.ban(user_id=user_to_ban.id, until_date=until_date)
    await message.reply(f"Пользователь @{user_to_ban.full_name} забанен на {time_str}.")

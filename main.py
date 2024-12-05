import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import dotenv_values
import random

token = dotenv_values(".env")["BOT_TOKEN"]
bot = Bot(token=token)
dp = Dispatcher()


@dp.message(Command("start"))
async def start_handler(message: types.Message):
    name = message.from_user.first_name
    await message.answer(f"Привет, {name}")



NAMES = ("Алексей", "Мария", "Иван", "София", "Дмитрий", "Анна")

@dp.message(Command("random"))
async def random_command(message: types.Message):
    random_name = random.choice(NAMES)

    await message.reply(f"Случайное имя: {random_name}")


@dp.message(Command("myinfo"))
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


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
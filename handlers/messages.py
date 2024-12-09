from aiogram import Router , types
from aiogram.filters import Command
import random

message_router = Router()


NAMES = ("Алексей", "Мария", "Иван", "София", "Дмитрий", "Анна")

@message_router.message(Command("random"))
async def random_command(message: types.Message):
    random_name = random.choice(NAMES)

    await message.reply(f"Случайное имя: {random_name}")
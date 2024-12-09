from aiogram import Router , types
from aiogram.filters import Command


start_router = Router()

@start_router.message(Command("start"))
async def start_handler(message: types.Message):
    name = message.from_user.first_name
    await message.reply(f"Добро пожаловать в наш ресторан! Для просмотра меню используйте команду /menu. {name}")

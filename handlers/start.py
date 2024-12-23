from aiogram import Router , types
from aiogram.filters import Command


start_router = Router()

@start_router.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer(f"Ваш ID: {message.from_user.id}")

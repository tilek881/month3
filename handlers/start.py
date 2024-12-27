from aiogram import Router , types
from aiogram.filters import Command


start_router = Router()

@start_router.message(Command("start"))
async def start_handler(message: types.Message):
    name = message.from_user.first_name
    await message.answer(f"Приветствую: @{name} , INLINE ВВОДЫ : /review , /menu , /order , /random , /myinfo , /admin")


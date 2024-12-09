from aiogram import Router, types
from aiogram.filters import Command

menu_router = Router()

@menu_router.message(Command("menu"))
async def menu_handler(message: types.Message) -> None:
    menu_text = (
        "Меню:\n"
        "1: 🥗Рамен - от 290 сом.\n"
        "2: 🍕Пицца - от 500 сом.\n"
        "3: 🍝Салат - от 300 сом.\n"
        "4: 🧃Напитки - от 100 сом.\n"
        "Для заказа используйте команду /order."
    )
    await message.reply(menu_text)

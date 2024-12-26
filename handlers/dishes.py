from aiogram import Router, types
from bot_config import manager
from aiogram.filters import Command


dishes_router = Router()

@dishes_router.message(Command("result"))
async def show_menu(message: types.Message):
    dishes = manager.dishes()
    if not dishes:
        await message.answer("Меню пока пустое.")
        return

    response = "📋_Меню_:\n\n"
    for dish in dishes:
        response += (
            f"🍴Название:*{dish[1]}*\n"
            f"💵Цена: {dish[2]} сом\n"
            f"📖Описание: {dish[3]}\n"
            f"📂Категория: {dish[4]}\n\n"
        )
    await message.answer(response, parse_mode="Markdown")

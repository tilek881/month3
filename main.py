import asyncio
from aiogram import Bot, Dispatcher
from dotenv import dotenv_values

from handlers.order import order_router
from handlers.info_command import command_router
from handlers.menu import menu_router
from handlers.messages import message_router
from handlers.start import start_router


token = dotenv_values(".env")["BOT_TOKEN"]
bot = Bot(token=token)
dp = Dispatcher()


async def main():
    dp.include_router(start_router) #ДЗ№2
    dp.include_router(message_router)
    dp.include_router(command_router)
    dp.include_router(menu_router) #ДЗ"№2
    dp.include_router(order_router) #ДЗ"№2
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
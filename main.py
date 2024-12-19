import asyncio


from handlers.order import order_router
from handlers.info_command import command_router
from handlers.menu import menu_router
from handlers.messages import message_router
from handlers.review_dialog import review_router, manager_db
from handlers.start import start_router
from bot_config import dp, bot,  manager


async def on_startup(bot):
    manager.create_table()



async def main():
    dp.include_router(start_router) #ДЗ"№2
    dp.include_router(message_router)
    dp.include_router(command_router)
    dp.include_router(menu_router) #ДЗ"№2
    dp.include_router(order_router) #ДЗ"№2
    dp.include_router(review_router) #ДЗ"№3

    dp.startup.register(on_startup)

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
from aiogram import Bot, Dispatcher
from dotenv import dotenv_values

from handlers.review_dialog import manager_db
from manager_db import Database


token = dotenv_values(".env")["BOT_TOKEN"]
bot = Bot(token=token)
dp = Dispatcher()



manager = Database("review.db")
manager_db.create_tables()


print("Initializing bot_config")
from manager_db import Database
try:
    manager = Database("review.db")
    print("Database manager initialized")
except Exception as e:
    print(f"Error initializing database manager: {e}")












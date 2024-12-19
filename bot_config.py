from aiogram import Bot, Dispatcher
from dotenv import dotenv_values
from manager_db import Database


token = dotenv_values(".env")["BOT_TOKEN"]
bot = Bot(token=token)
dp = Dispatcher()


manager = Database("review.db")
manager.create_table()















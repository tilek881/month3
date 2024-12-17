from aiogram import Bot, Dispatcher
from dotenv import dotenv_values
from handlers.db_manager import DatabaseManager


token = dotenv_values(".env")["BOT_TOKEN"]
bot = Bot(token=token)
dp = Dispatcher()

db_manager = DatabaseManager("reviews_w.db")















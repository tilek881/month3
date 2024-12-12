from aiogram import Router , types
from aiogram.filters import Command


order_router = Router()

@order_router.message(Command("order"))
async def order_handler(message: types.Message) -> None:

    await message.reply("Введите ваш заказ по номеру: 1:Рамен, 2:Пицца , "
                        "3:Салаты ,\n  4:Напитки. Мы свяжемся с вами для подтверждения!")


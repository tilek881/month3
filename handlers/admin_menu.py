from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from bot_config import manager


admin_router = Router()


admin_router.message.filter(F.from_user.id == 1559232214)
admin_router.callback_query.filter(F.from_user.id == 1559232214)


class Dish(StatesGroup):
    name = State()
    price = State()
    description = State()
    category = State()


@admin_router.message(Command("admin"))
async def start_add_dish(message: types.Message, state: FSMContext):
    await message.answer("Введите название блюда:")
    await state.set_state(Dish.name)


@admin_router.message(Dish.name)
async def set_dish_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text.strip())
    await message.answer("Введите цену блюда (только число):")
    await state.set_state(Dish.price)


@admin_router.message(Dish.price)
async def set_dish_price(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(price=int(message.text))
        await message.answer("Введите описание блюда:")
        await state.set_state(Dish.description)
    else:
        await message.answer("Цена должна быть числом. Попробуйте ещё раз.")


@admin_router.message(Dish.description)
async def set_dish_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text.strip())
    kb = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text='Супы')],
            [types.KeyboardButton(text='Горячие блюда')],
            [types.KeyboardButton(text='Холодные напитки')],
            [types.KeyboardButton(text='Горячие напитки')],
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer("Выберите категорию блюда:", reply_markup=kb)
    await state.set_state(Dish.category)


@admin_router.message(Dish.category)
async def set_dish_category(message: types.Message, state: FSMContext):
    await state.update_data(category=message.text.strip())
    data = await state.get_data()


    manager.insert_dish(
        name=data['name'],
        price=data['price'],
        description=data['description'],
        category=data['category']
    )

    await message.answer(
        f"Блюдо добавлено успешно:\n"
        f"Название: {data['name']}\n"
        f"Цена: {data['price']} сом.\n"
        f"Описание: {data['description']}\n"
        f"Категория: {data['category']}",
        reply_markup=types.ReplyKeyboardRemove()

    )
    await state.clear()
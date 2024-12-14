from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

review_router = Router()

class RestaurantReview(StatesGroup):
    name = State()
    phone_number = State()
    food_rating = State()
    cleanliness_rating = State()
    extra_comments = State()

@review_router.message(Command("review"))
async def start_review(message: types.Message, state: FSMContext):
    name_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Ввести имя", callback_data="enter_name")]
    ])
    await message.answer("Добро пожаловать в форму отзыва. Пожалуйста, введите ваше имя:", reply_markup=name_kb)
    await state.set_state(RestaurantReview.name)

@review_router.message(RestaurantReview.name)
async def save_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    contact_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Ввести номер телефона", callback_data="enter_phone"),
         InlineKeyboardButton(text="Ввести Инстаграм", callback_data="enter_instagram")]
    ])
    await message.answer("Введите ваш номер телефона или Инстаграм:", reply_markup=contact_kb)
    await state.set_state(RestaurantReview.phone_number)

@review_router.message(RestaurantReview.phone_number)
async def save_phone(message: types.Message, state: FSMContext):
    await state.update_data(phone_number=message.text)
    food_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Оценить качество еды", callback_data="rate_food")]
    ])
    await message.answer("Как вы оцениваете качество еды (1-5)?", reply_markup=food_kb)
    await state.set_state(RestaurantReview.food_rating)

@review_router.message(RestaurantReview.food_rating)
async def save_food_rating(message: types.Message, state: FSMContext):
    if message.text.isdigit() and 1 <= int(message.text) <= 5:
        await state.update_data(food_rating=message.text)
        clean_kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Оценить чистоту заведения", callback_data="rate_cleanliness")]
        ])
        await message.answer("Как вы оцениваете чистоту заведения (1-5)?", reply_markup=clean_kb)
        await state.set_state(RestaurantReview.cleanliness_rating)
    else:
        await message.answer("Пожалуйста, введите число от 1 до 5.")

@review_router.message(RestaurantReview.cleanliness_rating)
async def save_cleanliness_rating(message: types.Message, state: FSMContext):
    if message.text.isdigit() and 1 <= int(message.text) <= 5:
        await state.update_data(cleanliness_rating=message.text)
        comments_kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Добавить комментарии", callback_data="add_comments")]
        ])
        await message.answer("Если у вас есть дополнительные комментарии, напишите их. Если нет, напишите 'нет'.", reply_markup=comments_kb)
        await state.set_state(RestaurantReview.extra_comments)
    else:
        await message.answer("Пожалуйста, введите число от 1 до 5.")

@review_router.message(RestaurantReview.extra_comments)
async def save_extra_comments(message: types.Message, state: FSMContext):
    await state.update_data(extra_comments=message.text)
    data = await state.get_data()

    review_summary = (
        f"Спасибо за ваш отзыв!\n\n"
        f"Имя: {data.get('name')}\n"
        f"Контакт: {data.get('phone_number')}\n"
        f"Оценка еды: {data.get('food_rating')}\n"
        f"Оценка чистоты: {data.get('cleanliness_rating')}\n"
        f"Дополнительные комментарии: {data.get('extra_comments')}"
    )

    await message.answer(review_summary)
    await state.clear()

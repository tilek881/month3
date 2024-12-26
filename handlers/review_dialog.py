from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from manager_db import Database



review_router = Router()
manager_db = Database("review.db")

class RestaurantReview(StatesGroup):
    name = State()
    phone_number = State()
    food_rating = State()
    cleanliness_rating = State()
    extra_comments = State()

@review_router.message(Command("review"))
async def start_review(message: types.Message, state: FSMContext):
    await message.answer("Добро пожаловать в форму отзыва. Пожалуйста, введите ваше имя (от 2 до 50 символов):")
    await state.set_state(RestaurantReview.name)


@review_router.message(RestaurantReview.name)
async def save_name(message: types.Message, state: FSMContext):
    name = message.text.strip()
    if 2 <= len(name) <= 50:
        await state.update_data(name=name)
        await message.answer("Введите ваш номер телефона или Инстаграм:")
        await state.set_state(RestaurantReview.phone_number)
    else:
        await message.answer("Имя должно быть длиной от 2 до 50 символов. Пожалуйста, попробуйте снова.")


@review_router.message(RestaurantReview.phone_number)
async def save_phone(message: types.Message, state: FSMContext):
    await state.update_data(phone_number=message.text.strip())


    kb = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text='bad')],
            [types.KeyboardButton(text='good')]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer("Как вы оцениваете еду? Пожалуйста, выберите одну из кнопок.", reply_markup=kb)
    await state.set_state(RestaurantReview.food_rating)


@review_router.message(RestaurantReview.food_rating)
async def save_food_rating(message: types.Message, state: FSMContext):
    if message.text in ('bad', 'good'):
        await state.update_data(food_rating=message.text)
        await message.answer("Как вы оцениваете чистоту заведения (1-5)?", reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(RestaurantReview.cleanliness_rating)
    else:
        await message.answer("Пожалуйста, выберите один из вариантов: 'bad' или 'good'.")


@review_router.message(RestaurantReview.cleanliness_rating)
async def save_cleanliness_rating(message: types.Message, state: FSMContext):
    if message.text.isdigit() and 1 <= int(message.text) <= 5:
        await state.update_data(cleanliness_rating=int(message.text))
        await message.answer("Если у вас есть дополнительные комментарии, напишите их. Если нет, напишите 'нет'.")
        await state.set_state(RestaurantReview.extra_comments)
    else:
        await message.answer("Пожалуйста, введите число от 1 до 5.")


@review_router.message(RestaurantReview.extra_comments)
async def save_extra_comments(message: types.Message, state: FSMContext):
    await state.update_data(extra_comments=message.text.strip())
    data = await state.get_data()

    manager_db.insert_review(
        name=data['name'],
        contact=data['phone_number'],
        food_quality=data['food_rating'],
        cleanliness=data['cleanliness_rating'],
        comments=data['extra_comments']
    )
    await message.answer("Ваш отзыв сохранен. Спасибо!")


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
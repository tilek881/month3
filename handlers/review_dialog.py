from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

review_router = Router()

class RestourantReview(StatesGroup):
    name = State()
    phone_number = State()
    food_rating = State()
    cleanliness_rating = State()
    extra_comments = State()


@review_router.message(Command("review"))
async def start_review(message: types.Message,):
    review_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Ввести имя", callback_data="enter_name")],
        [InlineKeyboardButton(text="Телефон", callback_data="phone_number"),
         InlineKeyboardButton(text="Инстаграм", callback_data="instagram_username")],
        [InlineKeyboardButton(text="Оценить качество еды", callback_data="food_rating")],
        [InlineKeyboardButton(text="Оценить чистоту", callback_data="cleanliness_rating")]
    ])
    await message.answer("Добро пожаловать в форму отзыва. Выберите действие:", reply_markup=review_kb)




@review_router.callback_query()
async def handle_callback(callback: types.CallbackQuery, state: FSMContext):
    data = callback.data

    if data == "enter_name":
        await callback.message.answer("Введите ваше имя:")
        await state.set_state(RestourantReview.name)
    elif data == "phone_number":
        await callback.message.answer("Введите ваш номер телефона:")
        await state.set_state(RestourantReview.phone_number)
    elif data == "instagram_username":
        await callback.message.answer("Введите ваш Инстаграм:")
        await state.set_state(RestourantReview.phone_number)
    elif data == "food_rating":
        food_kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="1", callback_data="food_1"),
             InlineKeyboardButton(text="2", callback_data="food_2"),
             InlineKeyboardButton(text="3", callback_data="food_3"),
             InlineKeyboardButton(text="4", callback_data="food_4"),
             InlineKeyboardButton(text="5", callback_data="food_5")]
        ])
        await callback.message.answer("Как вы оцениваете качество еды (1-5)?", reply_markup=food_kb)
    elif data.startswith("food_"):
        rating = data.split("_")[1]
        await state.update_data(food_rating=rating)
        await callback.message.answer("Оценка качества еды сохранена. Выберите следующий шаг на клавиатуре.")
    elif data == "cleanliness_rating":
        clean_kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="1", callback_data="clean_1"),
             InlineKeyboardButton(text="2", callback_data="clean_2"),
             InlineKeyboardButton(text="3", callback_data="clean_3"),
             InlineKeyboardButton(text="4", callback_data="clean_4"),
             InlineKeyboardButton(text="5", callback_data="clean_5")]
        ])
        await callback.message.answer("Как вы оцениваете чистоту заведения (1-5)?", reply_markup=clean_kb)
    elif data.startswith("clean_"):
        rating = data.split("_")[1]
        await state.update_data(cleanliness_rating=rating)
        await callback.message.answer("Оценка чистоты сохранена. Выберите следующий.")



@review_router.message(RestourantReview.name)
async def save_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Имя сохранено. Выберите следующий шаг.")


@review_router.message(RestourantReview.phone_number)
async def save_contact(message: types.Message, state: FSMContext):
    await state.update_data(phone_number=message.text)
    await message.answer("Контакт сохранен. Выберите следующий шаг.")


@review_router.message(RestourantReview.extra_comments)
async def get_extra_comments(message: types.Message, state: FSMContext):
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
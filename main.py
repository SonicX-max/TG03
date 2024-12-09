import sqlite3
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command

# Замените токен вашего бота
TOKEN = "7728195333:AAGqVhy5pcY8DL8cKVrD6EvbcdDTKIf20iA"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Инициализация базы данных
def init_db():
    conn = sqlite3.connect("school_data.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            grade TEXT
        )
    """)
    conn.commit()
    conn.close()

# Функция для сохранения данных в базу
def save_to_db(name, age, grade):
    conn = sqlite3.connect("school_data.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO students (name, age, grade) VALUES (?, ?, ?)", (name, age, grade))
    conn.commit()
    conn.close()

# Состояния для общения с пользователем
user_data = {}

@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("Привет! Я бот для записи учеников. Введите ваше имя:")
    user_data[message.chat.id] = {}

@dp.message(F.text)
async def collect_data(message: Message):
    chat_id = message.chat.id

    if "name" not in user_data[chat_id]:
        user_data[chat_id]["name"] = message.text
        await message.answer("Введите ваш возраст:")
    elif "age" not in user_data[chat_id]:
        try:
            age = int(message.text)
            user_data[chat_id]["age"] = age
            await message.answer("Введите ваш класс (например, 10A):")
        except ValueError:
            await message.answer("Пожалуйста, введите корректный возраст в числовом формате.")
    elif "grade" not in user_data[chat_id]:
        user_data[chat_id]["grade"] = message.text
        name = user_data[chat_id]["name"]
        age = user_data[chat_id]["age"]
        grade = user_data[chat_id]["grade"]

        # Сохранение в базу данных
        save_to_db(name, age, grade)

        await message.answer(f"Данные сохранены: \nИмя: {name}\nВозраст: {age}\nКласс: {grade}")
        del user_data[chat_id]  # Сброс данных после сохранения

async def main():
    init_db()  # Инициализация базы данных
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
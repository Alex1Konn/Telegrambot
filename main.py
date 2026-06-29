#Создать БД- таблицу (id SERIAL, first_name, last_name, age, phone_number)
# БОТ на айограме для добавления людей по заданным пользователем

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
import psycopg2
import os
from dotenv import load_dotenv

# Подключение к базе данных PostgreSQL
bot = Bot(token=TELEGRAM_API_KEY)
dp = Dispatcher()

# Подключение к базе данных PostgreSQL
conn = psycopg2.connect(
    dbname="persondb",
    user="postgres",
    password="root",
    host="localhost"
)
cursor = conn.cursor()

#Хендлер  /start
@dp.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await message.answer(
        "Введите имя, фамилию, возраст и номер телефона через запятую:"
    )
    await state.set_state('waiting_for_data')

#Хендлер для обработки ответа пользователя
@dp.message(StateFilter('waiting_for_data'))
async def process_add_command(message: Message, state: FSMContext):
    user_input = message.text

def process_add_command(message):
    try:
        data = message.text.split(',')
        first_name = data[0].strip()
        last_name = data[1].strip()
        age = int(data[2].strip())

        cursor.execute('INSERT INTO person (first_name, last_name, age) VALUES (%s, %s, %s)', (first_name, last_name, age))
        conn.commit()
        bot.send_message(message.chat.id, f'{first_name} {last_name} добавлен в базу данных.')
    except Exception as e:
        bot.send_message(message.chat.id, "Ошибка при добавлении человека.")
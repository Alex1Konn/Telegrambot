#Создать БД- таблицу (id SERIAL, first_name, last_name, age, phone_number)
# БОТ на айограме для добавления людей по заданным пользователем

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import psycopg2

# Подключение к базе данных PostgreSQL
conn = psycopg2.connect(
    dbname="persondb",
    user="postgres",
    password="root",
    host="localhost"
)
cursor = conn.cursor()

import os
from dotenv import load_dotenv
import logging
import aiohttp
load_dotenv()
TELEGRAM_API_KEY=os.getenv("TELEGRAM_API_KEY")

class Form(StatesGroup):
    name = State()
# Обработчик команды /add для добавления человека
@dp.message(Сommand("start"))
async def cmd_star(message:Message, state: FSMContext):
    await  message.answer(
        "Введите имя, фамилию, возраст и номер телефона через запятую:"
    )
    await state.set_state(process_add_command)
    # bot.register_next_step_handler(msg, process_add_command) захват ответа пользователя в телеботе

@dp.message(Command(process_add_command))

"""
https://ru.stackoverflow.com/questions/1583720/%D1%84%D1%83%D0%BD%D0%BA%D1%86%D0%B8%D1%8F-bot-register-next-step-handler-%D0%B8%D0%B7-telagrambotapi
"""
#пример

@dp.message(Command())
async def cmd_start(message:Message):
    await message.answer(
        "Привет! Я бот который присылает картинки прямо из популярных сабреддитов!\n"
        "Используй  команды: \n"
        "/mem - получить слуйчайную картинку\n"
        "/help - показать помощь"
    )

@dp.message(Command("mem"))
async def cmd_mem(message:Message):

    мппп
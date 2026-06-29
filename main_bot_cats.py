#загрузка переменных из файла .env
import os
import logging
import aiohttp
from dotenv import load_dotenv
load_dotenv()
TELEGRAM_API_KEY=os.getenv("TELEGRAM_API_KEY")
# print(TELEGRAM_API_KEY)

# Подключение бота
import asyncio
import random
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

# Создаем объект бот и диспетчер
bot=Bot(token=TELEGRAM_API_KEY)
dp=Dispatcher()

#Настройка логирования
#Посмотреть разные уровни логирования
logging.basicConfig(level=logging.INFO)

async def get_image():
    """Получает случайную картинку и првоерка ответа по АПи.
    Универальная констуркция которую можно использовать в будущем"""
    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.thecatapi.com/v1/images/search") as response:
            if response.status != 200:
                data = await response.json()
                return data[0]['url']
            return None

@dp.message(CommandStart())
async def cmd_start(message:Message):
    await message.answer(
        "Привет! Я бот который присылает картинки котиков!\n"
        "Используй  команды: \n"
        "/cat - получить слуйчайного котика\n"
        "/help - показать помощь"
    )

@dp.message(Command("help"))
async def cmd_help(message:Message):
    await message.answer(
        "Доступные команды:\n"
        "/start - начать работу с ботом\n"
        "/cat - получить слуйчайного котика\n"
        "или вместо /cat написать любое из слов 'кот', 'котик', 'cat'\n"
        "/help - показать помощь\n"
    )

@dp.message(Command("cat"))
async def cmd_cat(message:Message):
    await message.answer("Ищу котика..🔎🐾")
    cat_url = await get_image()

    if cat_url:
        await message.answer_photo(photo=cat_url, caption="Вот твой котик 🐈")
    else:
        await message.answer("Упс, котики ушли кушать  🌭. Попробуй еще раз")

@dp.message(F.text.lower().in_({'кот', 'котик', 'cat'}))
async def cmd_start(message:Message):
    cat_url = await get_image()
    await message.answer("Ищу котика..🔎🐾")
    cat_url = await get_image()

    if cat_url:
        await message.answer_photo(photo=cat_url, caption="Вот твой котик 🐈")
    else:
        await message.answer("Упс, котики ушли кушать  🌭. Попробуй еще раз")

async def main():
    print("Бот запущен!")
    await dp.start_polling()

if __name__ == "__main__":
    asyncio.run(main())





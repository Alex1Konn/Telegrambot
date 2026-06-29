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
        async with session.get("https://meme-api.com/gimme") as response:
            if response.status != 200:
                data = await response.json()
                return data['url']
            return None

@dp.message(CommandStart())
async def cmd_start(message:Message):
    await message.answer(
        "Привет! Я бот который присылает картинки прямо из популярных сабреддитов!\n"
        "Используй  команды: \n"
        "/mem - получить слуйчайную картинку\n"
        "/help - показать помощь"
    )

@dp.message(Command("help"))
async def cmd_help(message:Message):
    await message.answer(
        "Доступные команды:\n"
        "/start - начать работу с ботом\n"
        "/мем - получить слуйчайную картинку\n"
        "или вместо /mem написать любое из слов 'картинка', 'мем', 'mem'\n"
        "/help - показать помощь\n"
    )

@dp.message(Command("mem"))
async def cmd_mem(message:Message):
    await message.answer("Ищу картинки..🔎")
    mem_url = await get_image()

    if mem_url:
        await message.answer_photo(photo=mem_url, caption="Вот мемчик для тебя!")
    else:
        await message.answer("Упс, пока не нашлось ничего забавного... Попробуй еще раз!")

@dp.message(F.text.lower().in_({'картинка', 'мем', 'mem'}))
async def cmd_start(message:Message):
    await message.answer("Ищу картинки..🔎")
    mem_url = await get_image()

    if mem_url:
        await message.answer_photo(photo=mem_url, caption="Вот мемчик для тебя!")
    else:
        await message.answer("Упс, пока не нашлось ничего забавного... Попробуй еще раз!")

async def main():
    print("Бот запущен!")
    await dp.start_polling()

if __name__ == "__main__":
    asyncio.run(main())





"""
# https://t.me/MyFirst16071990Bot
# создать файл .env
# pip install python-dotenv
# пото в ENV файле создать константу TELEGRAM_API_KEY= и вписать туда апи

#загрузка переменных из файла .env
import os
from dotenv import load_dotenv
load_dotenv()
TELEGRAM_API_KEY=os.getenv("TELEGRAM_API_KEY")
# print(TELEGRAM_API_KEY)

# Подключение бота
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

# Создаем объект бот и диспетчер
bot=Bot(token=TELEGRAM_API_KEY)
dp=Dispatcher()

# этот хендлер срабатывает на команду /start
@dp.message(Command(commands='start'))
async def process_start_command (message: Message):
    await message.answer("Привет! Это ЭХО-бот. \n Напиши что-нибудь.")
@dp.message(Command(commands='help'))
async def process_help_command (message: Message):
    await message.answer("Есть прблемы?")

@dp.message()
async def send_echo(message: Message):
    await message.reply(text=message.text)

# запуск бота
if __name__ == '__main__':
    dp.run_polling(bot)

"""



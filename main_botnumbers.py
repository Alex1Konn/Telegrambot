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
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message

import random
# Создаем объект бот и диспетчер
bot=Bot(token=TELEGRAM_API_KEY)
dp=Dispatcher()


ATTEMPTS = 5

user = {'in_game': False,
        'secret_number': None,
        'attempts': None,
        'total_games': 0,
        'wins': 0
        }

def get_random_number() -> int:
    return random.randint(1, 100)

# этот хендлер срабатывает на команду /start
@dp.message(Command(commands='start'))
async def process_start_command (message: Message):
    await message.answer("Привет!\n Давай играть в 'Угадай число'."
                         "Чтобы получить правило игры в список доступных\n"
                         "Отправить команду /help"
                         )

# этот хендлер срабатывает на команду /help
@dp.message(Command(commands='help'))
async def process_help_command (message: Message):
    await message.answer('Правила игры:\n\nЯ загадываю число от 1 до 100, '
        f'а вам нужно его угадать\nУ вас есть {ATTEMPTS} '
        'попыток\n\nДоступные команды:\n/help - правила '
        'игры и список команд\n/cancel - выйти из игры\n'
        '/stat - посмотреть статистику\n\nДавай сыграем?'
                         )

# этот хендлер срабатывает на команду /stat
@dp.message(Command(commands='stat'))
async def process_stat_command(message: Message):
    await message.answer(
        f"Всего игр сыграно: {user["total_games"]}\n"
        f"Игр выиграно: {user["wins"]}\n"
        )

@dp.message(Command(commands='cancel'))
async def process_cancel_command(message: Message):
    if user["in_game"]:
        user["in_game"] = False
        await message.answer(
            "Вы вышли из ишры. Если захотите сыграть"
            "снова напишите об этом"
        )
    else:
        await message.answer(
            "А мы и так с вами не играем. Может сыграем разок?"
        )

@dp.message(F.text.lower().in_(['да', 'давай', 'сыграем', 'играем', 'играть', 'хочу играть']))
async def process_positive_answer(message: Message):
    if not(user["in_game"]):
        user["in_game"] = True
        user["secret_number"] = get_random_number()
        user["attempts"] = ATTEMPTS
        await message.answer(
            "УРА! Я загадал число от 1 до 100. Попробуй угадать"
        )
    else:
        await message.answer(
            "Пока мы играем в игру я могу"
            "реагировать только на числа от 1 до 100"
            "и команды /cancel и /start"
        )

@dp.message(F.text.lower().in_(['нет', 'не', 'не хочу', 'не буду']))
async def process_negative_answer(message: Message):
    if not(user["in_game"]):
        await message.answer(
            "Жаль: (\n\n Если захотите поиграть - просто напишите об этом"
        )
    else:
        await message.answer(
            "Мы же сейчас с вами играем. Присылай, пожалуйста, числа от 1 до 100"
        )

@dp.message()
async def process_numbers_answer(message: Message):
    if user["in_game"]:
        if int(message.text) == user["secret_number"]:
            user["in_game"] = False
            user["total_games"] += 1
            user["wins"] += 1
            await message.answer(
                "УРА!!! Вы угададли число! \n\n"
                "Может сыграем  еще?"
            )

        elif int(message.text) > user["secret_number"]:
            user["attempts"] -=1
            await message.answer(
                "Мое число меньше"
                )
        elif int(message.text) < user["secret_number"]:
            user["attempts"] -= 1
            await message.answer(
                "Мое число больше"
            )

        if user['attempts'] == 0:
            user["in_game"] = False
            user["total_games"] += 1
            await message.answer(
                'К сожалению у вас больше не осталось попыток. Вы проиграли: \n\n'
                f'Мое число было {user["secret_number"]} \n\n Давай сыграем еще'
            )

    else:
        await message.answer("Мы еще не играем. Хотите играть")

@dp.message()
async def process_other_answer(message: Message):
    if user["in_game"]:
        await message.answer(
            "Мы же сейчас с вами играем"
            "Присылайте, пожалуйста, числа от 1 до 100"
        )
    else:
        await message.answer(
            "Я довольно ограченный бот, давайте просто сыграем"
        )

# запуск бота
if __name__ == '__main__':
    dp.run_polling(bot)
"""




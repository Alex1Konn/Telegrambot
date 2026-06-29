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
import asyncio
import random
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Создаем объект бот и диспетчер
bot=Bot(token=TELEGRAM_API_KEY)
dp=Dispatcher()
"""
#камень - ножницы - бумага
CHOICES = {
    "rock": {'emoji': "✊", "text":"камень"},
    "scissors": {'emoji': "✌️", "text":"ножницы"},
    "paper": {'emoji': "✋", "text":"бумага"}
}

def get_game_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="✊ Kамень", callback_data="game:rock")
    builder.button(text="️✌️ Ножницы", callback_data="game:scissors")
    builder.button(text="️✋ Бумага", callback_data="game:paper")
    builder.adjust(3)
    return builder.as_markup()

def determine_winner(user_choice:str, bot_choice:str):
    if user_choice == bot_choice:
        return "draw"

    wins = {
        "rock":"scissors",
        "scissors":"paper",
        "paper":"rock"
    }
    return "win" if wins[user_choice] == bot_choice else "lose"

@dp.message(CommandStart())
async def cmd_start(message:types.Message):
    await message.answer(
        "<b>Камень, Ножницы, Бумага!</b>\n\n"
        "Выбери свой ход:",
        reply_markup=get_game_keyboard(),
        parse_mode="HTML"
    )

@dp.callback_query(F.data.startswitch("game:"))
async def process_game(callback:types.CallbackQuery):
    user_choice = callback.data.split(":")[1]
    bot_choice = random.choice(list(CHOICES.keys()))

    result = determine_winner(user_choice, bot_choice)

    result_text = {
        "win": "🏆 <b> Ты победил! </b>",
        "lose": "⛈️ <b> Бот победил! </b>",
        "draw": "🤝 <b> Ничья! </b>"
    }

    text = (
        f"{result_text[result]}\n\n"
        f"Твой выбор {CHOICES[user_choice]['emoji']} {CHOICES[user_choice]['text']}\n"
        f"Выбор бота {CHOICES[bot_choice]['emoji']} {CHOICES[bot_choice]['text']}\n"
        f"Сыграть ещё?"
    )
    await callback.message.edit_text(
        text=text,
        reply_markup=get_game_keyboard(),
        parse_mode="html"
    )

    await callback.answer()
"""
 #камень-ножницы-бумага-ящерица-спок

CHOICES = {
    "rock": {'emoji': "✊", "text":"камень"},
    "scissors": {'emoji': "✌️", "text":"ножницы"},
    "paper": {'emoji': "✋", "text":"бумага"},
    "lizard": {'emoji': " 🦎", "text":"ящерица"},
    "Spock": {'emoji': "🖖", "text":"Спок"}
}

def get_game_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="✊ Kамень", callback_data="game:rock")
    builder.button(text="️✌️ Ножницы", callback_data="game:scissors")
    builder.button(text="️✋ Бумага", callback_data="game:paper")
    builder.button(text="️🦎 Ящерица", callback_data="game:lizard")
    builder.button(text="️🖖 Спок", callback_data="game:Spock")
    builder.adjust(5)
    return builder.as_markup()

def determine_winner(user_choice:str, bot_choice:str):
    if user_choice == bot_choice:
        return "draw"

    wins = {
        "rock":"scissors",
        "scissors":"paper",
        "paper":"rock",
        "lizard":"Spock",
        "Spock":"rock"
    }
    return "win" if wins[user_choice] == bot_choice else "lose"

@dp.message(CommandStart())
async def cmd_start(message:types.Message):
    await message.answer(
        "<b>Камень, Ножницы, Бумага, Ящериц, Спок!</b>\n\n"
        "Выбери свой ход:",
        reply_markup=get_game_keyboard(),
        parse_mode="HTML"
    )

@dp.callback_query(F.data.startswitch("game:"))
async def process_game(callback:types.CallbackQuery):
    user_choice = callback.data.split(":")[1]
    bot_choice = random.choice(list(CHOICES.keys()))

    result = determine_winner(user_choice, bot_choice)

    result_text = {
        "win": "🏆 <b> Ты победил! </b>",
        "lose": "⛈️ <b> Бот победил! </b>",
        "draw": "🤝 <b> Ничья! </b>"
    }

    text = (
        f"{result_text[result]}\n\n"
        f"Твой выбор {CHOICES[user_choice]['emoji']} {CHOICES[user_choice]['text']}\n"
        f"Выбор бота {CHOICES[bot_choice]['emoji']} {CHOICES[bot_choice]['text']}\n"
        f"Сыграть ещё?"
    )
    await callback.message.edit_text(
        text=text,
        reply_markup=get_game_keyboard(),
        parse_mode="html"
    )

    await callback.answer()
async def main():
    await dp.start_polling(bot)
# запуск бота
if __name__ == '__main__':
    asyncio.run(main())





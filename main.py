#Создать БД- таблицу (id SERIAL, first_name, last_name, age, phone_number)
# БОТ на айограме для добавления людей по заданным пользователем

"""
Цель: Переписать существующего бота для работы с базой данных PostgreSQL, используя современный асинхронный фреймворк aiogram 3.x.
Ограничения: Не использовать классы для состояний (использовать строки), сохранять синхронную работу с БД (psycopg2) для простоты.
Этап 1: Подготовка окружения и базовая структура
Задача: Настроить проект так, чтобы бот мог запуститься и отвечать на команду /start.
Установка библиотек:
Убедись, что установлены: aiogram, psycopg2-binary, python-dotenv.
Настройка токена:
Создай файл .env и запиши туда токен: TELEGRAM_API_KEY=твой_токен.
В коде используй load_dotenv() и os.getenv() для получения токена.
Инициализация:
Создай объекты Bot и Dispatcher.
Настрой подключение к PostgreSQL (conn, cursor).
Первый хендлер:
Напиши асинхронную функцию cmd_start, которая реагирует на команду /start.
Бот должен просто отвечать: "Бот запущен. Используйте команды /add, /show, /delete".
Запуск:
Добавь блок if __name__ == '__main__': с запуском dp.start_polling(bot).
Чек-поинт 1: Бот запускается без ошибок и отвечает на /start.
Этап 2: Реализация добавления человека (/add) через FSM
Задача: Научить бота принимать данные от пользователя пошагово, используя состояния.
Хендлер команды /add:
При получении команды отправляй сообщение: "Введите имя, фамилию, возраст и телефон через запятую".
Устанавливай состояние: await state.set_state("waiting_for_add_data").
Хендлер обработки текста:
Создай функцию, которая срабатывает только если у пользователя состояние "waiting_for_add_data".
Внутри функции:
Получи текст сообщения.
Раздели его по запятой (.split(',')).
Проверь, что элементов ровно 4. Если нет — отправь ошибку и не меняй состояние.
Преобразуй возраст в int.
Выполни INSERT в базу данных.
Отправь подтверждение: "Человек добавлен".
Важно: В конце вызови await state.clear(), чтобы сбросить состояние.
Обработка ошибок:
Оберни логику в try...except, чтобы бот не падал, если пользователь введет буквы вместо возраста.
Чек-поинт 2: Ты можешь написать /add, ввести данные, и они появляются в таблице person в pgAdmin. После этого бот снова готов принимать команды.
Этап 3: Просмотр списка людей (/show)
Задача: Вывести все записи из базы данных.
Хендлер команды /show:
Это простая команда, ей не нужно состояние.
Выполни SELECT * FROM person.
Получи все строки через fetchall().
Форматирование ответа:
Если список пустой, отправь: "База данных пуста".
Если есть данные, пройди по ним циклом и сформируй одну большую строку ответа (как в старом коде).
Отправь эту строку пользователю.
Чек-поинт 3: Команда /show выводит красивый список всех добавленных людей.
Этап 4: Удаление человека (/delete) через FSM
Задача: Реализовать удаление по ID, также используя состояние, чтобы не удалять лишнее.
Хендлер команды /delete:
Отправь сообщение: "Введите ID человека для удаления".
Установи состояние: await state.set_state("waiting_for_delete_id").
Хендлер обработки ID:
Срабатывает только при состоянии "waiting_for_delete_id".
Попробуй преобразовать текст в int.
Выполни DELETE FROM person WHERE id = %s.
Проверь, сколько строк было удалено (можно через cursor.rowcount).
Отправь подтверждение или сообщение, что такого ID нет.
Вызови await state.clear().
Чек-поинт 4: Ты можешь удалить человека по ID, и он исчезает из списка при команде /show.
Дополнительные рекомендации для Алекса:
Тестирование: После каждого этапа проверяй работу в Telegram. Не пиши весь код сразу!
Безопасность БД: Сейчас у тебя глобальный cursor. В больших проектах так не делают, но для учебного проекта это допустимо. Главное — не забывай делать conn.commit() после изменений (INSERT/DELETE).
Если застряла: Вспомни про state.clear(). Это самая частая ошибка новичков в FSM — бот "зависает" в состоянии и игнорирует другие команды

""""""

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
    # Устанавливаем состояние, так как класса нет.
    await state.set_state("waiting_for_data")

#Хендлер для обработки ответа пользователя
@dp.message(StateFilter("waiting_for_data"))
async def process_add_command(message: Message, state: FSMContext):
    try:
        data = message.text.split(',')

        # Проверка на количество элементов, чтобы не было ошибки IndexError
        if len(data) < 4:
            await message.answer("Пожалуйста, введите 4 значения через запятую.")
            return

        first_name = data[0].strip()
        last_name = data[1].strip()
        age = int(data[2].strip())
        phone = data[3].strip()

    cursor.execute(
        'INSERT INTO person (first_name, last_name, age, phone) VALUES (%s, %s, %s, %s)',
        (first_name, last_name, age, phone)
    )
    conn.commit()

    await message.answer(f'{first_name} {last_name} добавлен в базу данных.')

    except Exception as e:
        await message.answer(f"Ошибка при добавлении человека: {e}")
    finally:
        await state.clear()

if __name__ == '__main__':
    import asyncio
    asyncio.run(dp.start_polling(bot))
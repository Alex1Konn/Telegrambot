https://api.thecatapi.com/v1/images/search

import telebot
import psycopg2

# Подключение к базе данных PostgreSQL
conn = psycopg2.connect(
    dbname="persondb",
    user="postgres",
    password="root",
    host="localhost"
)
cursor = conn.cursor()

# Инициализация бота
bot = telebot.TeleBot("6734757548:AAHDkIQvnXMAvTN0f9f_MX9N4d3kIPlEm98")

# Обработчик команды /add для добавления человека
@bot.message_handler(commands=['add'])
def add_person(message):
    msg = bot.send_message(message.chat.id, "Введите имя, фамилию и возраст через запятую:")
    bot.register_next_step_handler(msg, process_add_command)

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


@bot.message_handler(commands=['show'])
def show_people(message):
    cursor.execute('SELECT * FROM person')
    people = cursor.fetchall()
    response = ''
    if not people:
        bot.send_message(message.chat.id, 'База данных пуста.')
    else:
        for person in people:
            response += f"Имя: {person[1]}, Фамилия: {person[2]}, Возраст: {person[3]}\n"
        bot.send_message(message.chat.id, response)


# Обработчик команды /delete для удаления человека по ID
@bot.message_handler(commands=['delete'])
def delete_person(message):
    msg = bot.send_message(message.chat.id, "Введите ID человека для удаления:")
    bot.register_next_step_handler(msg, process_delete_command)

def process_delete_command(message):
    try:
        person_id = int(message.text.strip())
        cursor.execute('DELETE FROM person WHERE id = %s', (person_id,))
        conn.commit()
        bot.send_message(message.chat.id, f'Человек с ID {person_id} удален из базы данных.')
    except Exception as e:
        bot.send_message(message.chat.id, "Ошибка при удалении человека.")

# Запуск бота
bot.polling()

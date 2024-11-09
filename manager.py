import numpy as np
import re

input_file = "wordList.txt"  # Путь к входному файлу. Пока что тестовая заглушка
# В будущем, вызываться будет из внешнего файла

# Todo: Подумать, что лучше: использовать тхт файл или хранить список слов в базе данных?
"""
Это файл-менеджер, где предварительно предлагаю собирать все "вспомогательные" функции
Такие как: преобразование текста, отправка текста в файл или в БД
Тут уже реализованы функции: 
    1. прочитать весь список слов с файла 
    2. преобразовать текст в нижний регистр и убрать все знаки препинания
    3. преобразовать текст в бинарный вектор. 
"""



def read_words_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        words = [line.strip().lower() for line in file]
    return words


def preprocess_text(text): # Нагло спиздил эту функцию с рабочего кода.
    text = re.sub(r'[^\w\s]', '', text)
    text = text.lower()
    return text


def text_to_binary_vector(text, word_list):
    vector_size = len(word_list)
    binary_vector = np.zeros(vector_size, dtype=int) # нулевой массив с целочисленными элементами (0\1) размера такого
    # сколько у нас слов в "словаре"

    for word in text.split():
        if word in word_list:
            binary_vector[word_list.index(word)] = 1

    return binary_vector


# Читаем слова из файла
word_list = read_words_from_file(input_file)

text = ("Да давай договоримся без лишних ушей."
        "Алло, это Сергей? Слушай, я тебе уже говорил, что нам нужно срочно решить вопрос с закупкой нового оборудования. Да, да, я знаю, что у нас есть тендер, но давай будем честными, ты и я оба понимаем, что это просто формальность."
        "Да, я уже поговорил с Андреем, он сказал, что готов подписать все документы, если мы сделаем ему \"небольшой подарок\". Ну, ты знаешь, как это обычно бывает."
        "Я уже нашел подходящую фирму, которая готова предоставить оборудование по цене, которая нам выгодна. Конечно, там будет небольшая разница, но это будет нашей \"комиссией\"."
        "Не волнуйся, все будет чисто оформлено. Мы просто укажем, что это \"дополнительные услуги\" или \"быстрое обслуживание\". Никто и слова не скажет."
        "Да, я знаю, что это рискованно, но что поделать? Это жизнь. Мы же не хотим, чтобы наши конкуренты получили этот контракт, верно?"
        "Ладно, давай созвонимся завтра, я тебе скину все детали. И не забудь, это наше с тобой дело, никому не говори ")

preprocessed_text = preprocess_text(text)

# Преобразуем текст в бинарный вектор
binary_vector = text_to_binary_vector(preprocessed_text, word_list)

# Выводим список слов и бинарный вектор
print("Список слов:", word_list)
print("Бинарный вектор:", binary_vector)

#СКРИПТ ДЛЯ ЗАПИСИ В БД POSTGRESS ПРОТОТИП
import psycopg2
from psycopg2 import sql

def connect_to_db():
    # Подключение к базе данных PostgreSQL
    conn = psycopg2.connect(
        dbname="your_db_name",  # имя базы данных
        user="your_user",       # имя пользователя
        password="your_password",  # пароль
        host="localhost",       # хост (localhost или IP адрес сервера)
        port="5432"             # порт по умолчанию
    )
    return conn

def insert_text_to_db(text):
    try:
        # Подключаемся к базе данных
        conn = connect_to_db()
        cursor = conn.cursor()

        # SQL запрос для вставки текста в таблицу
        insert_query = sql.SQL("INSERT INTO messages (text) VALUES (%s)")
        cursor.execute(insert_query, (text,))

        # Подтверждаем изменения
        conn.commit()

        print("Text successfully inserted into the database.")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Закрываем соединение с базой данных
        cursor.close()
        conn.close()

def read_lines_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()  # Читаем все строки в список
            return lines
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

# Пример использования для вставки нескольких строк
if __name__ == "__main__":
    file_path = 'path_to_your_file.txt'
    lines = read_lines_from_file(file_path)

    if lines:
        for line in lines:
            insert_text_to_db(line.strip())  # .strip() убирает лишние пробелы и символы новой строки


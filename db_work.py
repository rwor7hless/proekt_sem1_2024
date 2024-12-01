from xmlrpc.client import boolean

import fasttext
import psycopg2
from psycopg2 import sql

# Загрузка модели FastText
model = fasttext.load_model('../korr_analys/model.bin')

# Параметры подключения к базе данных PostgreSQL
DB_CONFIG = {
    'dbname': 'Anticorruption',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost',
    'port': '5432'
}

# Подключение к базе данных
def connect_to_db():
    return psycopg2.connect(**DB_CONFIG)

def analyze_and_update():
    try:
        # Подключение к базе данных
        connection = connect_to_db()
        cursor = connection.cursor()

        # Выбираем все записи с текстом из поля `content`
        select_query = "SELECT \"ID\", audio_content FROM \"Audio\" WHERE audio_content IS NOT NULL;"
        cursor.execute(select_query)
        rows = cursor.fetchall()

        # Анализ каждого текста
        for row in rows:
            record_id = row[0]
            content = row[1]

            # Предсказание FastText
            prediction = model.predict(content)
            is_corrupted = int(prediction[0][0][-1])  # 0 или 1
            percentage1 = round(prediction[1][0] * 100, 2)  # Уверенность модели в процентах
            percentage = float(percentage1)
            # Обновление записи в таблице
            update_query = """
                UPDATE \"Audio\"
                SET is_corrupted = %s, percentage = %s
                WHERE \"ID\" = %s;
            """
            cursor.execute(update_query, (is_corrupted, percentage, record_id))

        # Сохранение изменений
        connection.commit()
        print("Данные успешно обновлены.")

    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        if connection:
            cursor.close()
            connection.close()

# Запуск анализа и обновления
analyze_and_update()

import os
import whisper
import psycopg2
from psycopg2 import sql
from pathlib import Path

# Подключение к базе данных PostgreSQL
def connect_to_db():
    return psycopg2.connect(
        dbname="Anticorruption",  # Укажите имя вашей базы
        user="postgres",         # Ваше имя пользователя
        password="1337",     # Ваш пароль
        host="localhost",             # Хост базы данных
        port="5432"                   # Порт PostgreSQL (по умолчанию 5432)
    )

# Создание таблицы для хранения транскрипций
def create_table_if_not_exists(conn):
    with conn.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transcriptions (
                id SERIAL PRIMARY KEY,
                filename TEXT NOT NULL,
                transcription TEXT NOT NULL
            );
        """)
        conn.commit()

# Сохранение транскрипции в базу данных
def save_transcription_to_db(conn, filename, transcription):
    with conn.cursor() as cursor:
        cursor.execute("""
            INSERT INTO transcriptions (filename, transcription)
            VALUES (%s, %s);
        """, (filename, transcription))
        conn.commit()

# Транскрибирование аудиофайла
def transcribe_audio(file_path, model):
    print(f"Транскрибирование файла: {file_path}")
    result = model.transcribe(str(file_path))  # Преобразуем объект Path в строку
    return result['text']

# Основная функция
def main():
    # Путь к папке с mp3 файлами
    audio_folder = Path("C:/Users/pprol/proekt_sem1_2024/Audio")

    # Убедимся, что папка существует
    if not audio_folder.exists():
        print(f"Папка {audio_folder} не существует.")
        return

    # Загрузка модели Whisper
    model = whisper.load_model("base")  # Вы можете использовать "tiny", "small", "medium" или "large"

    # Подключение к базе данных
    try:
        conn = connect_to_db()
        print("Подключение к базе данных успешно!")
    except Exception as e:
        print(f"Ошибка подключения к базе данных: {e}")
        return

    create_table_if_not_exists(conn)

    # Перебор всех mp3 файлов в папке
    for file in audio_folder.glob("*.mp3"):
        print(f"Обрабатывается файл: {file}")

        # Проверка существования файла
        if not file.exists():
            print(f"Файл {file} не существует.")
            continue  # Пропустить этот файл и продолжить с другими

        try:
            transcription = transcribe_audio(file, model)
            save_transcription_to_db(conn, file.name, transcription)
            print(f"Транскрипция для {file.name} успешно сохранена в базу данных.")
        except Exception as e:
            print(f"Ошибка обработки файла {file.name}: {e}")

    # Закрытие соединения с базой данных
    conn.close()

if __name__ == "__main__":
    main()

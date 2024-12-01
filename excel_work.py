import fasttext
import pandas as pd

# Загрузка модели FastText
model = fasttext.load_model('../korr_analys/model.bin')


def classify_reviews_with_probability(input_file, output_file):
    """
    Классифицирует отзывы из файла Excel с использованием FastText, добавляет столбцы с меткой и вероятностью,
    и сохраняет результаты в новом файле.

    :param input_file: Путь к исходному файлу Excel (должен содержать столбец "0" с отзывами).
    :param output_file: Путь к выходному файлу Excel с добавленными столбцами "1" (метка) и "2" (вероятность).
    """
    # Загрузка данных из Excel файла
    df = pd.read_excel(input_file, usecols=[0], header=0)

    # Классификация отзывов с использованием модели FastText
    labels = []
    probabilities = []
    for review in df[0]:
        prediction = model.predict(str(review))
        label = prediction[0][0]  # Получаем метку (например, __label__1)
        probability = prediction[1][0]  # Получаем вероятность (например, 0.85)

        # Определяем метку 0 или 1 и вероятность в процентах
        if label == '__label__1':
            labels.append(1)
        else:
            labels.append(0)

        probabilities.append(probability * 100)  # Переводим вероятность в проценты

    # Добавление новых столбцов
    df[1] = labels  # Столбец "1" с метками 0 или 1
    df[2] = probabilities  # Столбец "2" с вероятностями в процентах

    # Сохранение обновленного DataFrame в новый Excel файл
    df.to_excel(output_file, index=False)


# Путь к входному и выходному файлам
input_file = 'test_data.xlsx'
output_file = 'test_data_3.xlsx'

# Классификация отзывов с метками и вероятностями, и сохранение результата
classify_reviews_with_probability(input_file, output_file)

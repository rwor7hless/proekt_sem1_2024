import pandas as pd
from sklearn.model_selection import train_test_split
import fasttext
import numpy as np  # Импорт NumPy для преобразования при необходимости

def load_word_list(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        word_list = file.read().splitlines()
    return word_list

# Загрузка данных из Excel файла
data = pd.read_excel('data.xlsx')

# Разделение данных на обучающую и тестовую выборки
train_data, test_data = train_test_split(data, test_size=0.2, random_state=42)

# Сохранение данных в текстовые файлы (FastText работает только с текстовыми файлами)
train_data.to_csv('train_fasttext.txt', header=None, index=None, sep=' ', mode='w')
test_data.to_csv('test_fasttext.txt', header=None, index=None, sep=' ', mode='w')

# Обучение модели
model = fasttext.train_supervised('train_fasttext.txt', epoch=50, lr=0.1, wordNgrams=2, dim=2, minCount=5, minn=3, maxn=5)

# Сохранение обученной модели
model.save_model("model.bin")

# Оценка качества модели на тестовой выборке
result = model.test('test_fasttext.txt')

# try-except, чтобы обработать случай деления на ноль
try:
    precision = result[1]
    recall = result[2]
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    print(f'Всего: {result[0]}')
    print(f'Точность: {precision:.4f}, Полнота: {recall:.4f}, F1-мера: {f1_score:.4f}')

except ZeroDivisionError:
    print('Error: Произошло деление на ноль. Точность, Полнота, и F1-мера неопределены.')

# Проверка работы модели на отзывах
for review in test_data[0].sample(min(len(test_data), 100)):  # Выбираем 100 случайных отзывов или меньше, если их недостаточно
    review = review.replace('\n', '')  # Убираем символы новой строки
    try:
        labels, probs = model.predict(review)
        labels = np.asarray(labels)  # Преобразуем список меток в массив
        probs = np.asarray(probs)    # Преобразуем список вероятностей в массив
        print(f'Отзыв: {review}\nПрогноз: {labels[0]}, Вероятность: {probs[0]:.4f}\n')
    except ValueError as e:
        print(f"Ошибка обработки отзыва: {review}\nПричина: {e}")

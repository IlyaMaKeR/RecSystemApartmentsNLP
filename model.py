import spacy
from nltk.corpus import stopwords
import nltk

# Загрузка ресурсов NLTK
nltk.download('stopwords')

def process_query(query):
    # Загружаем модель SpaCy для русского языка
    nlp = spacy.load("ru_core_news_sm")

    # Обрабатываем запрос
    doc = nlp(query)

    # Инициализируем список для тегов
    tags = []

    # Задаем стоп-слова
    stop_words = set(stopwords.words('russian'))
    sw = ['хотеть','желать','квартира','жильё']

    # Инициализируем переменные для объединения чисел и соответствующих слов
    current_number = None
    current_pos = None

    # Проходим по леммам токенов и добавляем их к тегам
    for token in doc:
        # Если токен - число, сохраняем его и его часть речи
        if token.pos_ == 'NUM':
            current_number = token.text
            current_pos = token.pos_
        # Если токен - существительное и перед ним идет число, объединяем их
        elif token.pos_ == 'NOUN' and current_number is not None:
            tags.append(f'{current_number} {token.lemma_}')
            current_number = None
        # Если токен - не стоп-слово и это не число, добавляем его к тегам
        elif token.lemma_.lower() not in stop_words and current_number is None:
            tags.append(token.lemma_)

    # Дополнительная проверка для завершения объединения числа и соответствующего слова
    if current_number is not None:
        tags.append(current_number)
    tags = [tag for tag in tags if tag not in sw and tag != ' ']

    return tags

import telebot
import db
import pymorphy3
import re

import NeighborSampler as ns
import log
import helpers as h

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.pipeline import make_pipeline
from config import TOKEN
telebot.apihelper.ENABLE_MIDDLEWARE = True
bot = telebot.TeleBot(TOKEN)
morph = pymorphy3.MorphAnalyzer(lang='ru')


answer_id = []
answer = dict()

for row in db.get_answers():
    answer[row[0]] = row[1]

questions = []
transform = 0

for row in db.get_questions():
    if transform % 50 == 0:
        print(f'{transform}\r', end='')
    # Если текст вопроса не пустой
    if row[0] > "":

        # Если в БД есть код ответа на вопрос
        if row[1] > 0:
            phrases = row[0]

            # разбираем вопрос на слова
            words = phrases.split(' ')
            phrase = ""

            for word in words:
                # каждое слово из вопроса приводим в нормальную словоформу
                word = morph.parse(word)[0].normal_form
                # составляем фразу из нормализованных слов
                phrase = phrase + word + " "

            # Если длина полученной фразы больше 0 добавляем ей в массив вопросов и массив кодов ответов
            if (len(phrase) > 0):
                questions.append(phrase.strip())
                answer_id.append(row[1])
                transform = transform + 1


# Векторизируем вопросы в огромную матрицу
# Перемножив фразы на слова из которых они состоят получим числовые значения
vectorizer_q = TfidfVectorizer()
vectorizer_q.fit(questions)
matrix_big_q = vectorizer_q.transform(questions)
print("Размер матрицы: ")
print(matrix_big_q.shape)


# Трансформируем матрицу вопросов в меньший размер для уменьшения объема данных
# Трансформировать будем в 200 мерное пространство, если вопросов больше 200
# Размерность подбирается индивидуально в зависимости от базы вопросов, которая может содержать 1 млн. или 1к вопросов и 1
# Без трансформации большая матрицу будет приводить к потерям памяти и снижению производительности
if transform > 200:
    transform = 200
print(transform)

svd_q = TruncatedSVD(n_components=transform)
svd_q.fit(matrix_big_q)

# получим трансформированную матрицу
matrix_small_q = svd_q.transform(matrix_big_q)
print("Коэффициент уменьшения матрицы: ")
print(svd_q.explained_variance_ratio_.sum())

# Поиск ответов
ns_q = ns.NeighborSampler()
ns_q.fit(matrix_small_q, answer_id)
pipe_q = make_pipeline(vectorizer_q, svd_q, ns_q)


''' START '''


@bot.message_handler(commands=['start'])
def start(message):
    text = "Привет, {0.first_name}! Поговорим?".format(message.from_user)
    bot.send_message(message.chat.id, text)

    log.bot(text, message.chat.id)


''' TEXT HANDLER '''

# Отвечаем на текст пользователя


@bot.message_handler(func=lambda message: True)
def get_text_messages(message):
    message.text = h.normalize_caseless(message.text)
    log.user(message)

    # разобьём фразу на массив слов, используя split. '\W' - любой символ кроме буквы и цифры
    words = re.split('\W', message.text)
    phrase = ""

    # разберем фразу на слова, нормализуем каждое и соберем фразу
    for word in words:
        word = morph.parse(word)[0].normal_form
        phrase = phrase + word + " "

    # получим код ответа вызывая нашу функцию
    reply_id = int(pipe_q.predict([phrase.strip()]))

    # отправим ответ
    bot.send_message(message.from_user.id, answer[reply_id])
    log.bot(answer[reply_id], message.chat.id)

    # if message.text =="не так":
    #     bot.send_message(message.from_user.id, "а как?")
    #     bot.register_next_step_handler(message, wrong)
    # else:
    #     result_say = s.answer_bot(message.text)

    # bot.send_message(message.chat.id, result_say[0])


''' FINISH '''

bot.polling(none_stop=True, interval=1)

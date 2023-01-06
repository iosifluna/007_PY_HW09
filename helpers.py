import unicodedata
import numpy as np


def normalize_caseless(text):
    '''Нормализуем переданный текст (символы левые убираем и заменяем)'''
    return unicodedata.normalize("NFKD", text.casefold())


def softmax(x):
    '''создание вероятностного распределения'''
    proba = np.exp(-x)

    return proba / sum(proba)

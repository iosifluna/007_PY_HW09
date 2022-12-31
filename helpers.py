import unicodedata
import numpy as np

# Нормализуем переданный текст (символы левые убираем и заменяем)
def normalize_caseless(text):
    return unicodedata.normalize("NFKD", text.casefold())


#создание вероятностного распределения
def softmax(x):
    proba = np.exp(-x)
        
    return proba / sum(proba)
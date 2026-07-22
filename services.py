from random import sample
from models import Word

def generate_random_words(count: int, difficult: str) -> list:
    words = Word.select().where(Word.difficulty == difficult)
    clean_words = [word.word for word in words]
    return sample(clean_words, k=count)


def cpm_func(time_sec: float, text):
    length = len(text)
    return round((length / time_sec) * 60)


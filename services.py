from random import sample
from models import Word


def generate_random_words(count: int, difficult: str) -> list:    
    words = Word.select().where(Word.difficulty == difficult)
    clean_words = [word.word for word in words]
    return sample(clean_words, k=count)


def cpm_func(time_sec: float, text):
    length = len(text)
    return round((length / time_sec) * 60)



def accuracy_func(original: str, typed: str) -> int:
    correct = sum(a == b for a, b in zip(original, typed))
    accuracy = (correct / len(original)) * 100
    return round(accuracy)

def user_time_func(time_spent: float) -> str:
    total_seconds = round(time_spent)
    minutes, seconds = divmod(total_seconds, 60)

    return f"{minutes:02d}:{seconds:02d}"




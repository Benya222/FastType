from random import sample
from models import Word

def generate_random_words(count, difficult):
    words = Word.select().where(Word.difficulty == difficult)
    clean_words = [word.word for word in words]
    return sample(clean_words, k=count)






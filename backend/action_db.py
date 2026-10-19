from models import init_db, PublicText, Word
from random import sample

''' READ '''
def get_all_public_texts():
    return PublicText.select()

def get_random_words(count: int, difficult: str) -> list:

    words = Word.select().where(Word.difficulty == difficult)
    clean_words = [word.word for word in words]
    
    return sample(clean_words, k=count)





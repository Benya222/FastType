from models import init_db, PublicText, Word
from random import sample

''' READ '''
def get_all_public_texts():
    return PublicText.select()

def get_summary_public_texts():
    return PublicText.select(PublicText.id, 
                             PublicText.title, 
                             PublicText.word_count, 
                             PublicText.char_count, 
                             PublicText.category, 
                             PublicText.tags)

def get_public_text_by_id(text_id: int):
    return PublicText.get_or_none(PublicText.id == text_id)

def get_random_words(count: int, difficult: str) -> list:

    words = Word.select().where(Word.difficulty == difficult)
    clean_words = [word.word for word in words]
    
    return sample(clean_words, k=count)





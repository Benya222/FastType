from models import Word


'''create'''
def add_words(words, difficult):
    data = [{'word': word, 'difficulty': difficult} for word in words]
    Word.insert_many(data).on_conflict_ignore().execute()    






# ===================================================


from models import Word, User


'''create'''
def add_words(words: list, difficult):
    data = [{'word': word, 'difficulty': difficult} for word in words]
    Word.insert_many(data).on_conflict_ignore().execute()    

def add_user(name: str, password: str):
    User.create(name= name, password= password)


'''read'''
def get_user_by_name(name: str) -> User:
    return User.select().where(User.name == name)


# ===================================================
def user_exists(name: str) -> bool:
    return User.select().where(User.name == name).exists()


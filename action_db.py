from models import Word, User, PersonalText, PersonalHistory
from peewee import fn

'''create'''
def add_words(words: list, difficult):
    data = [{'word': word, 'difficulty': difficult} for word in words]
    Word.insert_many(data).on_conflict_ignore().execute()    

def add_user(name: str, password: str):
    User.create(name= name, password= password)

def add_personal_text(title: str, text: str, user_id: int):
    characters = len(text)
    PersonalText.create(title= title, text= text, characters= characters, user= user_id)

def add_personal_history(user_id: int, text_title: str, cpm: int, accuracy: int):
    wpm = round(cpm / 5)
    PersonalHistory.create(text_title= text_title, cpm= cpm, wpm= wpm, accuracy= accuracy, user= user_id)

'''read'''
def get_user_by_name(name: str) -> User:
    return User.get(User.name == name)

# -------
def get_personal_texts(user_id: int):
    return PersonalText.select().where(PersonalText.user == user_id)

def get_personal_text_by_id(text_id: int, user_id: int):
    return PersonalText.get_or_none((PersonalText.id == text_id) & (PersonalText.user == user_id))

# --------
def get_personal_history(user_id: int):
    return PersonalHistory.select().where(PersonalHistory.user == user_id)

def get_max_cpm(user_id: int):
    return 


'''update'''
def edit_personal_text(title: str, text: str, text_id: int, user_id: int):
    PersonalText.update(title= title, text= text).where((PersonalText.id == text_id)&(PersonalText.user == user_id)).execute()

'''delete'''
def delete_personal_text(text_id: int, user_id: int):
    PersonalText.delete().where((PersonalText.id == text_id)&(PersonalText.user == user_id)).execute()    
# ===================================================
def user_exists(name: str) -> bool:
    return User.select().where(User.name == name).exists()


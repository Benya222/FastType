from peewee import *
from datetime import datetime
from utils import calculate_score

db = SqliteDatabase('fasttype.db')


class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    name = CharField()
    password = CharField()
    

class PersonalText(BaseModel):
    title = CharField()
    text = CharField()
    user = ForeignKeyField(User, backref="personal_text")

    @property
    def characters(self):
        return len(self.text)

class PersonalHistory(BaseModel):
    text_title = CharField()
    cpm = IntegerField()
    accuracy = IntegerField()
    completed_at = DateTimeField(default= datetime.now)
    user = ForeignKeyField(User, backref="personal_history")

    @property
    def score(self):
        return calculate_score(self.cpm, self.accuracy)

    @property
    def wpm(self):
        return round(self.cpm / 5)

class Word(BaseModel):
    word = CharField(unique= True)
    difficulty = CharField()    # easy, medium, hard


def init_db():
    db.connect()
    db.create_tables([User, PersonalText, PersonalHistory, Word])




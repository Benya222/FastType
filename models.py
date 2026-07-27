from peewee import *
from datetime import datetime


db = SqliteDatabase('fasttype.db')


class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    name = CharField()
    password = CharField()
    

class GeneralText(BaseModel):
    title = CharField()
    text = CharField()
    characters = IntegerField()

class PersonalText(BaseModel):
    title = CharField()
    text = CharField()
    characters = IntegerField()
    user = ForeignKeyField(User, backref="personal_text")

class PersonalHistory(BaseModel):
    text_title = CharField()
    cpm = IntegerField()
    wpm = IntegerField()
    accuracy = IntegerField()
    completed_at = DateTimeField(default= datetime.now)
    user = ForeignKeyField(User, backref="personal_history")

class Word(BaseModel):
    word = CharField(unique= True)
    difficulty = CharField()    # easy, medium, hard


def init_db():
    db.connect()
    db.create_tables([User, GeneralText, PersonalText, PersonalHistory, Word])




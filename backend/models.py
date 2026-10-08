from peewee import *
from datetime import datetime


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
    def char_count(self):
        return len(self.text)

class PersonalHistory(BaseModel):
    text_title = CharField()
    cpm = IntegerField()
    accuracy = FloatField()
    completed_at = DateTimeField(default= datetime.now)
    score = FloatField()
    user = ForeignKeyField(User, backref="personal_history")

    @property
    def wpm(self):
        return round(self.cpm / 5)

    @property
    def formatted_date(self):
        return self.completed_at.strftime('%d.%m.%Y')

    @property
    def formatted_time(self):
        return self.completed_at.strftime('%H:%M')

class Word(BaseModel):
    word = CharField(unique= True)
    difficulty = CharField()    # easy, medium, hard

class PublicText(BaseModel):
    title = CharField()
    text = CharField()
    category = CharField()
    tags = CharField()
    char_count = IntegerField()
    word_count = IntegerField()
    source_id = CharField(unique= True, null= True)


from peewee import *
from datetime import datetime


db = SqliteDatabase('fasttype')


class BaseModel(Model):
    class Meta:
        database = db


class GeneralText(BaseModel):
    title = CharField()
    text = CharField()
    characters = IntegerField()
    words = IntegerField()

class PersonalText(BaseModel):
    title = CharField()
    text = CharField()
    characters = IntegerField()
    words = IntegerField()

class PersonalHistory(BaseModel):
    text_title = CharField()
    cpm = IntegerField()
    wpm = IntegerField()
    accuracy = IntegerField()
    completed_at = DateTimeField(default= datetime.now)


def init_db():
    db.connect()
    db.create_tables([GeneralText, PersonalText, PersonalHistory])



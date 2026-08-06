from flask import session

def calculate_score(cpm: int, accuracy: int)-> float:
    return round(cpm * accuracy / 100, 2)


def is_logged():
    return 'user' in session


def valid_register(name, password):
    return name and len(password) >= 4

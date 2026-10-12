from models import init_db, PublicText

def get_all_public_texts():
    return PublicText.select()






if __name__ == "__main__":
    init_db()


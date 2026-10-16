''' Do imports in current directory '''
import os, sys

''' ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ '''
#==========================================================================
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)
#===========================================================================

''' Do imports in parent directory '''
from models import Word, db

''' ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ '''

EASY = 'easy'
MEDIUM = 'medium'
HARD = 'hard'


def import_words_list(words: list, difficult: str):
    data = [{'word': word, 'difficulty': difficult} for word in words]
    Word.insert_many(data).on_conflict_ignore().execute()      



if __name__ == "__main__":
    db.connect(reuse_if_open=True)
    db.create_tables([Word])
    try:
        import_words_list(..., ...)
    except Exception as e:
        print(e)
    finally:
        if not db.is_closed():
            db.close()


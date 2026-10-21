from flask import Flask, request
from models import init_db
from action_db import get_random_words
from utils import success_response, error_response
from service import ArgsValueError, PublicTextArgs, PublicTextService, list_of_public_text_to_dict

app = Flask(__name__)

init_db()

@app.get("/api/words")
def get_words():
    word_count = request.args.get('count', 10)
    difficult = request.args.get('difficult', 'medium')

    random_words = get_random_words(word_count, difficult)

    return success_response(data=random_words)


@app.get("/api/text")
def get_public_texts():

    text_args = PublicTextArgs(
        per_page= request.args.get('per_page', default= '20'),
        page= request.args.get('page', default= '1'),
        query= request.args.get('q'),
        from_word_count= request.args.get('from_w_count'),
        to_word_count=  request.args.get('to_w_count')
    )

    service = PublicTextService(text_args)
    texts, total_pages = service.fetch_texts()

    result_in_dict = list_of_public_text_to_dict(texts)
    meta = {
        "page": text_args.page,
        "per_page": text_args.per_page,
        "total_pages": total_pages,
        "has_next": total_pages > text_args.page
    }

    return success_response(data= result_in_dict, meta= meta)


@app.errorhandler(ArgsValueError)
def handle_args_error(error):
    return error_response(message= str(error), code=400)



app.run(debug=True)

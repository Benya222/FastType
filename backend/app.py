from flask import Flask, request
from models import init_db
from action_db import get_public_text_by_id
from utils import success_response, error_response
from service import (ArgsValueError,
                     NotFoundError, 
                     PublicTextArgs, 
                     PublicTextService, 
                     WordsArgs, 
                     WordsService,
                     to_full_dict,
                     to_summary_dict)


app = Flask(__name__)

init_db()

@app.get("/api/words")
def get_words():

    words_args = WordsArgs(
        count= request.args.get('count', 10),
        difficult= request.args.get('difficult', 'medium')
    )

    service = WordsService(words_args)
    words = service.fetch_random_words()

    return success_response(data=words)


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

    texts_in_dict = [to_summary_dict(text) for text in texts]
    meta = {
        "page": text_args.page,
        "per_page": text_args.per_page,
        "total_pages": total_pages,
        "has_next": total_pages > text_args.page
    }

    return success_response(data= texts_in_dict, meta= meta)


@app.get("/api/text/<text_id>")
def get_public_text(text_id):
    text = get_public_text_by_id(text_id)

    if text is None:
        raise NotFoundError(f"Text by '{text_id}' not found")

    return success_response(
        data= to_full_dict(text)
    )


@app.errorhandler(NotFoundError)
def handle_not_found_error(error):
    return error_response(message= str(error), code= 404)


@app.errorhandler(ArgsValueError)
def handle_args_error(error):
    return error_response(message= str(error), code=400)


app.run(debug=True)

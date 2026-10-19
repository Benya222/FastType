from flask import Flask, request
from action_db import get_random_words
from service import success_response, error_response

app = Flask(__name__)


@app.get("/api/words")
def get_words():
    word_count = request.args.get('count', 10)
    difficult = request.args.get('difficult', 'medium')

    random_words = get_random_words(word_count, difficult)

    return success_response(data=random_words)


@app.get("/api/text")
def get_public_texts():
    query = request.args.get('q', None)
    from_word_count = request.args.get('from_w_count', None)
    to_word_count = request.args.get('to_w_count', None)
    per_page = request.args.get('per_page', 20)
    page = request.args.get('page', 1)





app.run(debug=True)

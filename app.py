from flask import Flask, render_template, request
from services import generate_random_words, cpm_func
from models import init_db

app = Flask(__name__)

init_db()

@app.route('/', methods= ['GET', 'POST'])
def index():
    text = " ".join(generate_random_words(10, 'easy'))
    cpm = 0
    if request.method == 'POST':
        time_spent = request.form.get('time_spent')
        user_text = request.form.get('user_text')
        words_count = request.form.get('words_count')
        difficulty = request.form.get('difficulty')

        if words_count and difficulty:
            words_count = int(words_count)
            text = " ".join(generate_random_words(words_count, difficulty))

        if time_spent and user_text:
            time_spent_sec = float(time_spent)
            cpm = cpm_func(time_spent_sec, user_text)    


    return render_template('index.html', target_text = text, cpm= cpm) 
            


@app.route('/login')
def login():
    return 


@app.route('/register')
def register():
    return




app.run(debug=True)

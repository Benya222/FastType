from flask import Flask, render_template, request, session, redirect, url_for
from services import generate_random_words, cpm_func, accuracy_func, user_time_func
from action_db import *
from models import init_db
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "laldsodeik*"

init_db()

#-------------------------------
def is_logged():
    return 'user' in session


#-------------------------------







@app.route('/', methods= ['GET', 'POST'])
def index():
    cpm = 0
    accuracy = 0
    user_time = "00:00"
    user_char = 0


    if request.method == 'POST':
        time_spent = request.form.get('time_spent')
        user_text = request.form.get('user_text')
        words_count = request.form.get('words_count', 10)
        difficulty = request.form.get('difficulty', 'easy')

        if time_spent and user_text:
            time_spent_sec = float(time_spent)
            cpm = cpm_func(time_spent_sec, user_text)
            original = session['original_text']
            accuracy = accuracy_func(original, user_text)
            user_char = len(user_text)
            user_time = user_time_func(time_spent_sec)

        words_count = int(words_count)
        text = " ".join(generate_random_words(words_count, difficulty))
        session["original_text"] = text            

    else:
        text = " ".join(generate_random_words(10, 'easy'))
        session["original_text"] = text

    return render_template(
                            'index.html', 
                            target_text = text, 
                            cpm= cpm, 
                            accuracy= accuracy, 
                            user_char= user_char,
                            user_time= user_time,
                            logged= is_logged()
                            ) 
            


@app.route('/register', methods= ['GET', 'POST'])
def register():

    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')

        if user_exists(name):
            # flash
            return redirect(url_for('register'))

        else:
            hash_pass = generate_password_hash(password)
            add_user(name, hash_pass)
            # flash
            return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods= ['GET', 'POST'])
def login():

    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')

        if not user_exists(name):
            # flash
            return redirect(url_for('login'))

        user = get_user_by_name(name)
        if not check_password_hash(user.password, password):
            #flash
            return redirect(url_for('login'))

        session['user'] = user.name
        #flash
        return redirect(url_for('index'))

    return render_template('login.html')


@app.route('/logout')
def loguot():
    session.pop('user')
    #flash
    return redirect(url_for('login'))


app.run(debug=True)

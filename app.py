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
    personal_texts = None
    text_id = None
    text_obj = None

    if is_logged():
        user_id = session['user']
        personal_texts = get_personal_texts(user_id)

    if request.method == 'POST':
        time_spent = request.form.get('time_spent')
        user_text = request.form.get('user_text')
        words_count = request.form.get('words_count', 10, type= int)
        difficulty = request.form.get('difficulty', 'easy')
        text_id = request.form.get('text')

        if time_spent and user_text:
            time_spent_sec = float(time_spent)
            cpm = cpm_func(time_spent_sec, user_text)
            original = session.get('original_text')
            accuracy = accuracy_func(original, user_text)
            user_char = len(user_text)
            user_time = user_time_func(time_spent_sec)

        text= None
        if text_id and is_logged():
            text_obj = get_personal_text_by_id(text_id, session['user'])
            text = text_obj.text

        if not text:
            text = " ".join(generate_random_words(words_count, difficulty))
            text_id = None

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
                            personal_texts= personal_texts,
                            text_id= text_id,
                            logged= is_logged()
                            ) 
            


@app.route('/register', methods= ['GET', 'POST'])
def register():

    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')
        print(request.form)
        print(name)
        print(password)

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

        session['user'] = user.id
        #flash
        return redirect(url_for('index'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user')
    #flash
    return redirect(url_for('index'))


@app.route('/add_text', methods= ['GET', 'POST'])
def add_text():

    if request.method == 'POST':
        title = request.form.get('title')
        text = request.form.get('text')

        if title and text:
            add_personal_text(title, text, session['user'])
            #flash
            return redirect(url_for('index'))
        else:
            #flash
            return redirect(url_for('add_text'))

    return render_template('add_text.html')



@app.route('/edit/<id>')
def edit(id):
    return render_template('edit.html')

@app.route('/delete/<id>')
def delete(id):
    return redirect(url_for('index'))



app.run(debug=True)

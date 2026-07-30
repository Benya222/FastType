from flask import Blueprint, render_template, request, session, redirect, url_for
from services import generate_random_words, cpm_func, accuracy_func, user_time_func
from action_db import *



text_bp = Blueprint('text', __name__, template_folder='templates')


#-------------------------------
def is_logged():
    return 'user' in session
#-------------------------------

@text_bp.route('/', methods= ['GET', 'POST'])
def index():
    cpm = 0
    accuracy = 0
    user_time = "00:00"
    user_char = 0
    personal_texts = None
    text_id = None
    text_obj = None

    if is_logged():
        user_id = session.get('user')
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
                            'text/index.html', 
                            target_text = text,
                            cpm= cpm, 
                            accuracy= accuracy, 
                            user_char= user_char,
                            user_time= user_time,
                            personal_texts= personal_texts,
                            text_id= text_id,
                            logged= is_logged()
                            ) 
            

@text_bp.route('/add_text', methods= ['GET', 'POST'])
def add_text():

    if request.method == 'POST':
        title = request.form.get('title')
        text = request.form.get('text')

        if title and text:
            add_personal_text(title, text, session['user'])
            #flash
            return redirect(url_for('text.index'))
        else:
            #flash
            return redirect(url_for('text.add_text'))

    return render_template('text/add_text.html', logged= is_logged())



@text_bp.route('/edit/<id>', methods= ['GET', 'POST'])
def edit(id):
    user_id = session.get('user')
    current_text_obj = get_personal_text_by_id(id, user_id)
    current_title = current_text_obj.title
    current_text = current_text_obj.text
    if request.method == 'POST':
        new_title = request.form.get('title')
        new_text = request.form.get('text')

        edit_personal_text(new_title, new_text, id, user_id)
        #flash
        return redirect(url_for('text.index'), logged= is_logged())


    return render_template('text/edit.html', 
                           current_title= current_title,
                           current_text= current_text,
                           )

@text_bp.route('/delete/<id>')
def delete(id):
    user_id = session.get('user')
    delete_personal_text(id, user_id)
    #flash

    return redirect(url_for('text.index'))



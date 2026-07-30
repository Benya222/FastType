from flask import Blueprint, render_template, request, session, redirect, url_for
from services import generate_random_words, cpm_func, accuracy_func, user_time_func
from action_db import *



text_bp = Blueprint('text', __name__, template_folder='templates')


#-------------------------------
def is_logged():
    return 'user' in session
#-------------------------------

# @text_bp.route('/', methods= ['GET', 'POST'])
# def index():
#     cpm = 0
#     accuracy = 0
#     user_time = "00:00"
#     user_char = 0
#     personal_texts = None
#     text_id = None

#     if is_logged():
#         user_id = session.get('user')
#         personal_texts = get_personal_texts(user_id)

#     if request.method == 'POST':
#         time_spent = request.form.get('time_spent')
#         user_text = request.form.get('user_text')
#         words_count = request.form.get('words_count', 10, type= int)
#         difficulty = request.form.get('difficulty', 'easy')
#         text_id = request.form.get('text')

#         if time_spent and user_text:
#             time_spent_sec = float(time_spent)
#             cpm = cpm_func(time_spent_sec, user_text)
#             original = session.get('original_text')
#             accuracy = accuracy_func(original, user_text)
#             user_char = len(user_text)
#             user_time = user_time_func(time_spent_sec)

#         text= None
#         if text_id and is_logged():
#             text_obj = get_personal_text_by_id(text_id, session['user'])
#             text = text_obj.text

#         if not text:
#             text = " ".join(generate_random_words(words_count, difficulty))
#             text_id = None

#         session["original_text"] = text            
#     else:
#         text = " ".join(generate_random_words(10, 'easy'))
#         session["original_text"] = text
 
#     return render_template(
#                             'text/index.html', 
#                             target_text = text,
#                             cpm= cpm, 
#                             accuracy= accuracy, 
#                             user_char= user_char,
#                             user_time= user_time,
#                             personal_texts= personal_texts,
#                             text_id= text_id,
#                             logged= is_logged()
#                             ) 
            


# ================================================================
# 1. СТРАНИЦА ТРЕНАЖЕРА (Отображение)
# ================================================================
@text_bp.route('/', methods=['GET'])
def index():
    user_id = session.get('user') if is_logged() else None
    personal_texts = get_personal_texts(user_id) if user_id else None


    if 'current_test' not in session:
        default_text = " ".join(generate_random_words(10, 'easy'))
        session['current_test'] = {
            'text': default_text,
            'title': 'words 10(easy)',
            'text_id': None
        }

    current_test = session.get('current_test')
    target_text = current_test.get('text')

    if not target_text and current_test.get('text_id') and user_id:
        text_obj = get_personal_text_by_id(current_test['text_id'], user_id)
        if text_obj:
            target_text = text_obj.text
 
    last_result = session.pop('last_result', None)

    return render_template(
        'text/index.html', 
        target_text=target_text,
        text_id=session['current_test'].get('text_id'),
        personal_texts=personal_texts,
        logged=is_logged(),

        cpm=last_result['cpm'] if last_result else 0,
        accuracy=last_result['accuracy'] if last_result else 0,
        user_char=last_result['user_char'] if last_result else 0,
        user_time=last_result['user_time'] if last_result else "00:00"
    )


@text_bp.route('/start', methods=['POST'])
def start_test():
    words_count = request.form.get('words_count', 10, type=int)
    difficulty = request.form.get('difficulty', 'easy')
    text_id = request.form.get('text')

    selected_text = None
    title = f"words {words_count}({difficulty})"


    if text_id and is_logged():
        text_obj = get_personal_text_by_id(text_id, session['user'])
        if text_obj:
            title = getattr(text_obj, 'title', f"Personal Text #{text_id}")

    else:
        selected_text = " ".join(generate_random_words(words_count, difficulty))
        text_id = None

    session['current_test'] = {
        'text': selected_text,
        'title': title,
        'text_id': text_id
    }

    return redirect(url_for('text.index'))



@text_bp.route('/save', methods=['POST'])
def save_result():
    time_spent = request.form.get('time_spent')
    user_text = request.form.get('user_text')
    current_test = session.get('current_test')
    user_id = session.get('user')

    if time_spent and user_text and current_test:
        time_spent_sec = float(time_spent)
        original_text = current_test['text']

        if not original_text:
            text_obj = get_personal_text_by_id(current_test['text_id'], user_id)
            original_text = text_obj.text

        cpm = cpm_func(time_spent_sec, user_text)
        accuracy = accuracy_func(original_text, user_text)
        user_char = len(user_text)
        user_time = user_time_func(time_spent_sec)

        if is_logged():
            add_personal_history(user_id, current_test['title'], cpm, accuracy)


        session['last_result'] = {
            'cpm': cpm,
            'accuracy': accuracy,
            'user_char': user_char,
            'user_time': user_time
        }

    return redirect(url_for('text.index'))





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



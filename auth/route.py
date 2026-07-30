from flask import Blueprint, render_template, request, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from action_db import *


auth_bp = Blueprint('auth', __name__, template_folder='templates')

#-------------------------------
def is_logged():
    return 'user' in session
#-------------------------------

@auth_bp.route('/register', methods= ['GET', 'POST'])
def register():

    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')
        print(request.form)
        print(name)
        print(password)

        if user_exists(name):
            # flash
            return redirect(url_for('auth.register'))

        else:
            hash_pass = generate_password_hash(password)
            add_user(name, hash_pass)
            # flash
            return redirect(url_for('auth.login'))

    return render_template('auth/register.html')

@auth_bp.route('/login', methods= ['GET', 'POST'])
def login():

    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')

        if not user_exists(name):
            # flash
            return redirect(url_for('auth.login'))

        user = get_user_by_name(name)
        if not check_password_hash(user.password, password):
            #flash
            return redirect(url_for('auth.login'))

        session['user'] = user.id
        #flash
        return redirect(url_for('text.index'))

    return render_template('auth/login.html', logged= is_logged())


@auth_bp.route('/logout')
def logout():
    session.pop('user')
    #flash
    session.pop('current_test')
    return redirect(url_for('text.index'))


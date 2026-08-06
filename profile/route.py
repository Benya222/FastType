from flask import Blueprint, render_template, request, session, redirect, url_for
from utils import is_logged


profile_bp = Blueprint('profile', __name__, template_folder= 'templates')





@profile_bp.route('/profile/<user_id>')
def profile(user_id):
    if not is_logged():
        return redirect('text.index')

    

    return render_template('profile/profile.html')




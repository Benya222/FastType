from flask import Blueprint, render_template, request, session, redirect, url_for
from utils import is_logged
from action_db import get_personal_history, get_max_score, get_user_by_id


profiles_bp = Blueprint('profiles', __name__, template_folder= 'templates')





@profiles_bp.route('/profile/<user_id>')
def profile(user_id):
    if not is_logged():
        return redirect('text.index')
    
    user = get_user_by_id(user_id)
    best_score = get_max_score(user_id)
    personal_history = list(get_personal_history(user_id))


    

    return render_template('profiles/profile.html', 
                           user_name= user.name, 
                           best_score= best_score if best_score else '0000',
                           history= personal_history
                           )




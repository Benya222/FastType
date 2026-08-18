from flask import Flask
from models import init_db
from auth.route import auth_bp
from text.route import text_bp
from profiles.route import profiles_bp

app = Flask(__name__)
app.secret_key = "laldsodeik*"

init_db()


app.register_blueprint(text_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(profiles_bp)

 


app.run(debug=True)

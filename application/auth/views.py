from flask import Blueprint, render_template

auth = Blueprint('auth', __name__, template_folder='templates')


@auth.route('/')
def index():
    return render_template("auth/login.html")

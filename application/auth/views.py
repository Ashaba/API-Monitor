from flask import Blueprint, render_template, jsonify
from application.auth.helpers import (token_required, update_user)

auth = Blueprint('auth', __name__, template_folder='templates')


@auth.route('/')
def login():
    context = dict()
    context["title"] = "Dashboard"
    return render_template("auth/login.html", context=context)


@auth.route('/auth', methods=['POST'])
@token_required
@update_user
def authenticate():
    return jsonify(dict(status="success", message="login successful"))


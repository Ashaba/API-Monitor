from flask import Blueprint, render_template, jsonify, session, request
from application.auth.helpers import (update_user)

auth = Blueprint('auth', __name__, template_folder='templates')


@auth.route('/')
def login():
    context = dict()
    context["title"] = "API-Monitor | Login"
    session.clear()
    return render_template("auth/login.html", context=context)


@auth.route('/auth', methods=['POST'])
def authenticate():
    try:
        payload = request.get_json()
        update_user(payload)
        session['email'] = payload.get("email")
        session['name'] = payload.get("fullName")
        response = jsonify(dict(
            status="success",
            message="login successful"
        ))
        response.status_code = 200
        return response
    except Exception as e:
        response = jsonify(dict(
            status="fail",
            message=str(e),
        ))
        response.status_code = 400
        return response


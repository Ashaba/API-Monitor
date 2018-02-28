import logging
from flask import request, jsonify, g, session
from application.auth.models import User
from functools import wraps
from os import makedirs
import requests


LOGGER = logging.getLogger(__name__)
FORMATTER = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
makedirs('logs', exist_ok=True)
FILE_HANDLER = logging.FileHandler('logs/auth.log')
FILE_HANDLER.setFormatter(FORMATTER)
STREAM_HANDLER = logging.StreamHandler()
STREAM_HANDLER.setFormatter(FORMATTER)
LOGGER.setLevel(logging.DEBUG)
LOGGER.addHandler(FILE_HANDLER)
LOGGER.addHandler(STREAM_HANDLER)
INVALID_TOKEN_MSG = (
    "Authorization failed due to an Invalid token. Log into an Andela "
    "product's website and inspect it's cookies for a valid token.")
NO_BEARER_MSG = (
    "Invalid Token. The token should begin with the word 'Bearer '."
)
NO_TOKEN_MSG = (
    "Bad request. Header does not contain an authorization token. Log into"
    " an Andela product's website and inspect it's cookies for a token.")
SERVER_ERROR_MSG = 'Authorization failed. Please contact support.'


def save_user():
    user = User.query.filter_by(email=session.get("email")).first()
    if not user:
        user = User(
            name=session.get("name"),
            email=session.get("email"),
            image_url=session.get("image_url")
        )
        user.save()
    return user


def update_user(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user = User.query.filter_by(email=session.get("email")).first()
        if user:
            if user.image_url != session.get("image_url"):
                setattr(user, 'image_url', session.get("image_url"))
            if user.name != session.get("name"):
                setattr(user, 'name', session.get("name"))
            user.save()
        save_user()
        return f(*args, **kwargs)
    return decorated
    

def verify_token(token):
    url = "https://www.googleapis.com/oauth2/v3/tokeninfo?id_token="+token
    req = requests.get(url)
    if req.status_code == 200:
        try:
            data = req.json()
            return data
        except TypeError as e:
            return None
    return None


def current_user():
    try:
        user = User.query.filter_by(email="jnashaba4@gmail.com").first()
        # user = User.query.filter_by(email=session.get("email")).first()
        if user:
            return user
        return None
    except Exception as e:
        print(e)
        return None

    
# authorization decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # check that the Authorization header is set
        authorization_token = request.headers.get('Authorization')
        if not authorization_token:
            response = jsonify({
                "status": "fail",
                "data": {"message": "Please provide token"}
            })
            response.status_code = 401
            return response

        user = verify_token(request.headers['Authorization'])
        if not user:
            response = jsonify({
                "status": "fail",
                "data": {"message": "Invalid token"}
            })
            response.status_code = 401
            return response
        session['name'] = user["name"]
        session['email'] = user["email"]
        session['image_url'] = user["picture"]
        return f(*args, **kwargs)
    return decorated
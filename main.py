import os
import logging

from flask import Flask
from flask_migrate import Migrate
import threading
import time

from config import app_configuration

from application import models
from application.views import app_view
from application.auth.views import auth
from application.helpers import collection_scheduler

os.sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# You must configure these 3 values from Google APIs console
# https://code.google.com/apis/console
GOOGLE_CLIENT_ID = '886619612646-5uteafhidohmbkd2fej7fdfl0iso5vgd.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = 'sx1hzvBhxhj_PHRfo5jVwWYn'
REDIRECT_URI = '/dashboard'  # one of the Redirect URIs from Google APIs console


def create_application(environment):
    app = Flask(
        __name__,
        instance_relative_config=True,
        static_folder="application/static")
    app.config.from_object(app_configuration[environment])
    app.register_blueprint(app_view)
    app.register_blueprint(auth)
    # initialize SQLAlchemy
    models.db.init_app(app)

    # initilize migration commands
    Migrate(app, models.db)
    return app


app = create_application(os.getenv("FLASK_CONFIG") or "development")


@app.before_first_request
def active_job():
    def run_job():
        while True:
            time.sleep(10)
            collection_scheduler(app.app_context())
    thread = threading.Thread(target=run_job)
    thread.start()
    

def start_runner():
    def start_loop():
        while True:
            logging.info('In start loop')
            collection_scheduler(app.app_context())
            time.sleep(10)

    logging.info('Started runner')
    thread = threading.Thread(target=start_loop)
    thread.start()


if __name__ == "__main__":
    environment = os.getenv("FLASK_CONFIG")
    app = create_application(environment)
    start_runner()
    app.run()

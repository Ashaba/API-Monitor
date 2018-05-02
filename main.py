import os

from celery import Celery
from flask import Flask
from flask_migrate import Migrate

from config import app_configuration
from application import models
from application.views import app_view
from application.auth.views import auth

os.sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

GOOGLE_CLIENT_ID = '886619612646-5uteafhidohmbkd2fej7fdfl0iso5vgd.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = 'sx1hzvBhxhj_PHRfo5jVwWYn'
REDIRECT_URI = '/dashboard'  # one of the Redirect URIs from Google APIs console

celery = Celery(__name__, broker=os.environ.get('CELERY_BROKER_URL'))


def create_application(environment):
    app = Flask(
        __name__,
        instance_relative_config=True,
        static_folder="application/static")
    app.config.from_object(app_configuration[environment])
    app.register_blueprint(app_view)
    app.register_blueprint(auth)
    celery.conf.update(app.config)
    models.db.init_app(app)
    Migrate(app, models.db)
    return app


app = create_application(os.getenv("FLASK_CONFIG") or "development")


if __name__ == "__main__":
    environment = os.getenv("FLASK_CONFIG")
    app = create_application(environment)
    app.run()

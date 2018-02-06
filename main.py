import os

from flask import Flask
from flask_migrate import Migrate

from config import app_configuration

from application import models
from application.views import app_view
from application.auth.views import auth

os.sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def create_application(environment):
	app = Flask(__name__, instance_relative_config=True, static_folder="application/static")
	app.config.from_object(app_configuration[environment])
	app.register_blueprint(app_view)
	app.register_blueprint(auth)
	# initialize SQLAlchemy
	models.db.init_app(app)
	
	# initilize migration commands
	Migrate(app, models.db)

	return app


app = create_application(os.getenv("FLASK_CONFIG") or "development")


if __name__ == "__main__":
	environment = os.getenv("FLASK_CONFIG")
	app = create_application(environment)
	app.run()

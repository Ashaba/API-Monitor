import os

from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api

from config import app_configuration

from application import models

os.sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def create_application(environment):
	app = Flask(__name__, instance_relative_config=True, static_folder=None)
	app.config.from_object(app_configuration[environment])
	
	# initialize SQLAlchemy
	models.db.init_app(app)
	
	# initilize migration commands
	Migrate(app, models.db)
	
	# initilize api resources
	application = Api(app)
	
	@app.route('/')
	def login():
		return 'Login Page'

	return app


app = create_application(os.getenv("FLASK_CONFIG") or "development")


if __name__ == "__main__":
	environment = os.getenv("FLASK_CONFIG")
	app = create_application(environment)
	app.run()

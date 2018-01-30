import os

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell

from application.models import Collection, User, db
from main import create_application

environment = os.getenv("FLASK_CONFIG")
app = create_application(environment)

migrate = Migrate(app, db)

# Initialize flask script
manager = Manager(app)


def shell_command():
    """
    Add models to the shell command

    Args:
        None

    Returns:
      (dict) dictionary that include the specified models

    """
    models = [
        User, Collection
    ]
    zipped_models = zip(models, models)
    return dict(zipped_models)


# wraps function (shell_command) in shell command
manager.add_command('shell', Shell(make_context=shell_command))

# migrations
manager.add_command('db', MigrateCommand)

# if __name__ == '__main__':
manager.run()

import os
from main import create_application, celery


app = create_application(os.getenv('FLASK_CONFIG') or 'development')
app.app_context().push()

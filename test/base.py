from flask_testing import TestCase

from application.models import db
from main import create_application


class BaseTestCase(TestCase):

    def create_app(self):
        self.app = create_application('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        return self.app

    def setUp(self):
        db.drop_all()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

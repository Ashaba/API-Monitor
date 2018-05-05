from test.base import BaseTestCase
from application.helpers import valid_url, make_request
from application.models import Response


class TestHelpers(BaseTestCase):
	def test_valid_url(self):
		valid_url_test = valid_url("http://test.com")
		self.assertTrue(valid_url_test)
		
	def test_invalid_url(self):
		invalid_url_test = valid_url("test.com")
		self.assertFalse(invalid_url_test)
		
	def test_make_request(self):
		req = make_request("http://test.com", "GET")
		self.assertIsInstance(req, Response)
		
	def test_make_request_invalid_url(self):
		req = make_request("test.com", "GET")
		self.assertEqual(req, None)

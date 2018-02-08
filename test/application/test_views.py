from ..base import BaseTestCase


class TestApplication(BaseTestCase):
	def test_dashboard(self):
		response = self.client.get('/dashboard')
		self.assert200(response)

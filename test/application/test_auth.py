from test.base import BaseTestCase, user_payload
import json


class TestAuth(BaseTestCase):
	
	def test_authenticate(self):
		response = self.client.post('/auth', data=json.dumps(user_payload), content_type='application/json')
		response_data = json.loads(response.data)
		self.assert200(response)
		self.assertEqual(response_data["status"], "success")
		
	def test_auth_with_no_data(self):
		response = self.client.post('/auth', content_type='application/json')
		self.assert400(response)
		response_data = json.loads(response.data)
		self.assertEqual(response_data["status"], "fail")

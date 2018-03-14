from ..base import BaseTestCase, user_payload, request_payload
import json


class TestApplication(BaseTestCase):
	
	def test_get_dashboard(self):
		self.client.post('/auth', data=json.dumps(user_payload), content_type='application/json')
		response = self.client.get('/dashboard')
		self.assert_template_used('dashboard.html')
		self.assert200(response)
	
	def test_post_dashboard(self):
		self.client.post('/auth', data=json.dumps(user_payload), content_type='application/json')
		response = self.client.post('/dashboard', data=json.dumps(request_payload), content_type='application/json')
		response_data = json.loads(response.data)
		self.assertEqual(response_data["status"], "success")
		self.assert200(response)
		
	def test_get_dashboard_unauthenticated(self):
		response = self.client.get('/dashboard')
		self.assertEqual(response.status_code, 302)
		
	def test_get_team_view(self):
		self.client.post('/auth', data=json.dumps(user_payload), content_type='application/json')
		response = self.client.get('/team')
		self.assert_template_used('team.html')
		self.assert200(response)
		
	def test_get_team_unauthorized(self):
		response = self.client.get('/team')
		self.assertEqual(response.status_code, 302)
		
	def test_get_collection_view(self):
		self.client.post('/auth', data=json.dumps(user_payload), content_type='application/json')
		response = self.client.get('/collections')
		self.assert_template_used('collections.html')
		self.assert200(response)
		
	def test_get_collection_unauthorized(self):
		response = self.client.get('/collections')
		self.assertEqual(response.status_code, 302)

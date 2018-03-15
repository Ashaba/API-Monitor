from ..base import BaseTestCase, user_payload
import json


class TestApplication(BaseTestCase):
	
	def test_get_dashboard(self):
		self.client.post('/auth', data=json.dumps(user_payload), content_type='application/json')
		response = self.client.get('/dashboard')
		self.assert_template_used('dashboard.html')
		self.assert200(response)
		
	def test_get_dashboard_unauthenticated(self):
		response = self.client.get('/dashboard')
		self.assertEqual(response.status_code, 302)
	
	def test_get_results(self):
		self.client.post('/auth', data=json.dumps(user_payload), content_type='application/json')
		response = self.client.get('/results/1')
		self.assertEqual(response.status_code, 200)
		
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

from ..base import BaseTestCase, user_payload
import json
from application.models import db, Collection, Header, Request, RequestAssertion, Team
from application.auth.models import User


class TestApplication(BaseTestCase):
	checks = [
		{
			"method":"GET",
			"id":"",
			"url":"https://lmap-staging-test.andela.com/api/v1/careers",
			"headers":[
				{
					"key":"Token",
					"value":"someToken",
					"id":""
				}
			],
			"assertions":[
				{
					"assertion_type":"Status Code",
					"comparison":"equal (number)",
					"value":"200",
					"id":""
				}
			]
		}
	]

	def setUp(self):
		db.drop_all()
		db.create_all()
		self.user = User(name=user_payload['fullName'], email=user_payload['email'], image_url=user_payload['imageUrl'])
		self.user.save()

		self.team = Team(name="Test team", user_id=self.user.id)
		self.team.save()

		self.collection_one = Collection(name="collection one", user_id=self.user.id, team_id=self.team.id)
		self.collection_one.save()

		self.collection_two = Collection(name="collection two", user_id=self.user.id)
		self.collection_two.save()

	def test_get_dashboard(self):
		self.client.post('/auth', data=json.dumps(user_payload), content_type='application/json')
		response = self.client.get('/dashboard')
		self.assert_template_used('dashboard.html')
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

	def test_get_collections_correct_user_successful(self):
		self.client.post('/auth', data=json.dumps(user_payload), content_type='application/json')
		response = self.client.get('/collections')
		self.assertEqual(response.status_code, 200)
		self.assertTrue(self.get_context_variable('context')['collections'])
		self.assertListEqual(self.get_context_variable('context')['collections'],
							[self.collection_one, self.collection_two])

	def test_get_collections_different_user_no_result(self):
		another_user_payload = {
			"fullName": "Another User",
			"email": "another_user@gmail.com",
			"imageUrl": "another_image_random"
		}
		self.client.post('/auth', data=json.dumps(another_user_payload), content_type='application/json')
		response = self.client.get('/collections')
		self.assertEqual(response.status_code, 200)
		self.assertFalse(self.get_context_variable('context')['collections'])
		self.assertListEqual(self.get_context_variable('context')['collections'], [])

	def test_post_collections_unauthorized(self):
		response = self.client.post('/collections')
		self.assertEqual(response.status_code, 302)

	def test_post_collection_no_team_successful(self):
		self.client.post('/auth', data=json.dumps(user_payload), content_type='application/json')
		response = self.client.post('/collections', data=dict(team="none", collection="this is a test collection"))
		self.assertEqual(response.status_code, 200)
		self.assertTrue(self.get_context_variable('context')['collections'])
		self.assertEqual(len(self.get_context_variable('context')['collections']), 3)

	def test_post_collection_with_team_successful(self):
		self.client.post('/auth', data=json.dumps(user_payload), content_type='application/json')
		response = self.client.post('/collections', data=dict(team=self.team.name,
																collection="this is a test collection"))
		self.assertEqual(response.status_code, 200)
		self.assertTrue(self.get_context_variable('context')['collections'])
		self.assertEqual(len(self.get_context_variable('context')['collections']), 3)

	def test_post_collection_duplicate_name_with_team(self):
		self.client.post('/auth', data=json.dumps(user_payload), content_type='application/json')
		response = self.client.post('/collections', data=dict(team=self.team.name,
																collection="collection one"))
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.data, b'duplicate_collection')

	def test_post_collection_duplicate_name_no_team(self):
		self.client.post('/auth', data=json.dumps(user_payload), content_type='application/json')
		response = self.client.post('/collections', data=dict(team="none", collection="collection one"))
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.data, b'duplicate_collection')

	def test_delete_collection_unauthorized(self):
		response = self.client.delete('/collections')
		self.assertEqual(response.status_code, 302)

	def test_delete_collection_successful(self):
		self.client.post('/auth', data=json.dumps(user_payload), content_type='application/json')
		response = self.client.delete('/collections?id={}'.format(self.collection_one.id))
		self.assertEqual(response.status_code, 200)
		self.assertTrue(self.get_context_variable('context')['collections'])
		self.assertEqual(len(self.get_context_variable('context')['collections']), 1)
		self.assertListEqual(self.get_context_variable('context')['collections'], [self.collection_two])

	def test_post_check(self):
		self.client.post('/auth', data=json.dumps(user_payload), content_type='application/json')
		collection = Collection(name='Test Collection', user_id=self.user.id)
		collection.save()
		old_number_of_checks = len(collection.requests)
		
		self.checks[0]['id'] = ""
		response = self.client.post(
			f'/collection-details/{collection.id}/update',
			data=json.dumps(self.checks), content_type='application/json')
		self.assertEqual(response.status_code, 200)
		new_number_of_checks = len(collection.requests)
		self.assertEqual(new_number_of_checks, old_number_of_checks + 1)

	def test_update_check(self):
		self.client.post('/auth', data=json.dumps(user_payload), content_type='application/json')
		collection = Collection(name='Test Collection', user_id=self.user.id)
		collection.save()
		request = Request(
			collection_id=collection.id,
			method='GET',
			url='https://test.com',
		)
		request.save()
		old_number_of_headers = len(request.headers)
		self.checks[0]['id'] = f"{request.id}"
		response = self.client.post(
			f'/collection-details/{collection.id}/update',
			data=json.dumps(self.checks), content_type='application/json')
		self.assertEqual(response.status_code, 200)
		new_number_of_headers = len(request.headers)
		self.assertEqual(new_number_of_headers, old_number_of_headers + 1)

	def test_fetch_collection_details(self):
		self.client.post('/auth', data=json.dumps(user_payload), content_type='application/json')
		collection = Collection(name='Test Collection', user_id=self.user.id)
		collection.save()
		response = self.client.get(f'/collection-details/{collection.id}')
		self.assertEqual(response.status_code, 200)
		self.assertTrue('checks' in self.get_context_variable('context'))
		self.assertTrue('results' in self.get_context_variable('context'))
		self.assertEqual(self.get_context_variable('context')['collection_name'], collection.name)

	def test_post_check_with_duplicate_method_and_url(self):
		self.client.post('/auth', data=json.dumps(user_payload), content_type='application/json')
		collection = Collection(name='Test Collection', user_id=self.user.id)
		collection.save()
		request = Request(
			collection_id=collection.id,
			method='GET',
			url='https://test.com',
		)
		request.save()
		old_number_of_checks = len(collection.requests)
		self.checks[0][''] = f"{request.id}"
		self.checks[0]['method'] = 'GET'
		self.checks[0]['url'] = 'https://test.com'
		response = self.client.post(
			f'/collection-details/{collection.id}/update',
			data=json.dumps(self.checks), content_type='application/json')
		self.assertEqual(response.status_code, 200)
		new_number_of_checks = len(collection.requests)
		self.assertEqual(old_number_of_checks, new_number_of_checks)
		self.assertTrue((json.loads(response.data))['errors'])

	def test_post_duplicate_header(self):
		self.client.post('/auth', data=json.dumps(user_payload), content_type='application/json')
		collection = Collection(name='Test Collection', user_id=self.user.id)
		collection.save()
		request = Request(
			collection_id=collection.id,
			method='GET',
			url='https://lmap-staging-test.andela.com/api/v1/careers',
		)
		request.save()
		header = Header(key="Token", value="someToken", request_id=request.id)
		header.save()
		old_number_of_headers = len(request.headers)
		self.checks[0]['id'] = f"{request.id}"
		response = self.client.post(
			f'/collection-details/{collection.id}/update',
			data=json.dumps(self.checks), content_type='application/json')
		self.assertEqual(response.status_code, 200)
		new_number_of_headers = len(request.headers)
		self.assertEqual(old_number_of_headers, new_number_of_headers)
		self.assertTrue((json.loads(response.data))['errors'])

	def test_post_duplicate_assertion(self):
		self.client.post('/auth', data=json.dumps(user_payload), content_type='application/json')
		collection = Collection(name='Test Collection', user_id=self.user.id)
		collection.save()
		request = Request(
			collection_id=collection.id,
			method='GET',
			url='https://lmap-staging-test.andela.com/api/v1/careers',
		)
		request.save()
		assertion = RequestAssertion(
			assertion_type='Status Code',
			comparison='equal (number)',
			value=200,
			request_id=request.id
		)
		assertion.save()
		old_number_of_assertions = len(request.assertions)
		self.checks[0]['id'] = f"{request.id}"
		response = self.client.post(
			f'/collection-details/{collection.id}/update',
			data=json.dumps(self.checks), content_type='application/json')
		self.assertEqual(response.status_code, 200)
		new_number_of_assertions = len(request.assertions)
		self.assertEqual(old_number_of_assertions, new_number_of_assertions)
		self.assertTrue((json.loads(response.data))['errors'])

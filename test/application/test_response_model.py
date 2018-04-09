from ..base import BaseTestCase
from application.models import Response


class TestResponseModel(BaseTestCase):

	def setUp(self):
		super(TestResponseModel, self).setUp()
		self.test_response = Response(
			request_id="1",
			status_code="200",
			status="success",
			failures=0,
			response_time=1,
			data='some data',
			headers='some headers',
			response_summary_id=1
		)

	def test_create_request(self):
		old_response = Response.fetch_all()
		self.assertEqual(len(old_response), 0)
		self.test_response.save()
		current_response = Response.fetch_all()
		self.assertEqual(len(current_response), len(old_response) + 1)
	
	def test_update_request(self):
		self.test_response.save()
		response = Response.get(self.test_response.id)
		old_response_status_code = response.status_code
		response.status_code = 404
		response.save()
		new_response_status_code = Response.get(self.test_response.id)
		self.assertEqual(new_response_status_code.status_code, 404)
		self.assertNotEqual(old_response_status_code, new_response_status_code)
	
	def test_delete_request(self):
		self.test_response.save()
		old_responses = Response.fetch_all()
		particular_response = Response.find_first(id=self.test_response.id)
		particular_response.delete()
		current_responses = Response.fetch_all()
		self.assertNotEqual(len(old_responses), len(current_responses))
		self.assertEqual(len(current_responses), 0)

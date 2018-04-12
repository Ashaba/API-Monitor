from ..base import BaseTestCase, db
from application.models import Header, Request


class TestRequestModel(BaseTestCase):

	def setUp(self):
		super(TestRequestModel, self).setUp()
		self.request = Request(
			collection_id="1",
			method="GET",
			body="{'data': 'success'}",
			url="https://andela.com"
		)
	
	def test_create_request(self):
		old_request = Request.fetch_all()
		self.assertEqual(len(old_request), 0)
		self.request.save()
		current_request = Request.fetch_all()
		self.assertEqual(len(current_request), len(old_request) + 1)
		
	def test_update_request(self):
		self.request.save()
		request = Request.get(self.request.id)
		old_request_url = request.url
		request.url = "https://test.com"
		request.save()
		current_request = Request.get(request.id)
		self.assertEqual(current_request.url, "https://test.com")
		self.assertNotEqual(old_request_url, current_request.url)
		
	def test_delete_request(self):
		self.request.save()
		old_requests = Request.fetch_all()
		particular_request = Request.find_first(id=self.request.id)
		particular_request.delete()
		current_requests = Request.fetch_all()
		self.assertNotEqual(len(old_requests), len(current_requests))
		self.assertEqual(len(current_requests), 0)

from test.base import BaseTestCase
from application.models import ResponseAssertion


class TestResponseAssertionModel(BaseTestCase):

	def setUp(self):
		super(TestResponseAssertionModel, self).setUp()
		self.test_response_assertion = ResponseAssertion(
			response_id="1",
			request_assertion_id="1",
			assertion_type="Status Code",
			comparison="equal",
			status="success",
			value=200
		)

	def test_create_response_assertion(self):
		old_response_assertions = ResponseAssertion.fetch_all()
		self.assertEqual(len(old_response_assertions), 0)
		self.test_response_assertion.save()
		current_response_assertions = ResponseAssertion.fetch_all()
		self.assertEqual(len(current_response_assertions), len(old_response_assertions) + 1)
	
	def test_update_response_assertion(self):
		self.test_response_assertion.save()
		response_assertion = ResponseAssertion.get(self.test_response_assertion.id)
		old_response_assertion_status = response_assertion.comparison
		response_assertion.comparison = 'less than'
		response_assertion.save()
		new_response_assertion_status = ResponseAssertion.get(self.test_response_assertion.id)
		self.assertEqual(new_response_assertion_status.comparison, 'less than')
		self.assertNotEqual(old_response_assertion_status, new_response_assertion_status)
	
	def test_delete_response_assertion(self):
		self.test_response_assertion.save()
		old_response_assertions = ResponseAssertion.fetch_all()
		particular_response_assertion = ResponseAssertion.find_first(id=self.test_response_assertion.id)
		particular_response_assertion.delete()
		current_response_assertions = ResponseAssertion.fetch_all()
		self.assertNotEqual(len(old_response_assertions), len(current_response_assertions))
		self.assertEqual(len(current_response_assertions), 0)

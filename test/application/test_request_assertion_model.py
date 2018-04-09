from ..base import BaseTestCase
from application.models import RequestAssertion


class TestRequestAssertionModel(BaseTestCase):

	def setUp(self):
		super(TestRequestAssertionModel, self).setUp()
		self.test_request_assertion = RequestAssertion(
			request_id="1",
			assertion_type="Status Code",
			comparison="equal",
			value=200
		)

	def test_create_request_assertion(self):
		old_request_assertions = RequestAssertion.fetch_all()
		self.assertEqual(len(old_request_assertions), 0)
		self.test_request_assertion.save()
		current_request_assertions = RequestAssertion.fetch_all()
		self.assertEqual(len(current_request_assertions), len(old_request_assertions) + 1)
	
	def test_update_request_assertion(self):
		self.test_request_assertion.save()
		request_assertion = RequestAssertion.get(self.test_request_assertion.id)
		old_request_assertion_comparison = request_assertion.comparison
		request_assertion.comparison = 'less than'
		request_assertion.save()
		new_request_assertion_comparison = RequestAssertion.get(self.test_request_assertion.id)
		self.assertEqual(new_request_assertion_comparison.comparison, 'less than')
		self.assertNotEqual(old_request_assertion_comparison, new_request_assertion_comparison)
	
	def test_delete_request_assertion(self):
		self.test_request_assertion.save()
		old_request_assertions = RequestAssertion.fetch_all()
		particular_request_assertion = RequestAssertion.find_first(id=self.test_request_assertion.id)
		particular_request_assertion.delete()
		current_request_assertions = RequestAssertion.fetch_all()
		self.assertNotEqual(len(old_request_assertions), len(current_request_assertions))
		self.assertEqual(len(current_request_assertions), 0)

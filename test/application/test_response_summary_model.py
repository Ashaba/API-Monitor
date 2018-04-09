from ..base import BaseTestCase
from application.models import ResponseSummary


class TestResponseSummaryModel(BaseTestCase):

	def setUp(self):
		super(TestResponseSummaryModel, self).setUp()
		self.test_response_summary = ResponseSummary(
			status="success",
			failures=0,
			run_from='Schedule',
			collection_id=1
		)

	def test_create_response_summary(self):
		old_response_summary = ResponseSummary.fetch_all()
		self.assertEqual(len(old_response_summary), 0)
		self.test_response_summary.save()
		current_response_summary = ResponseSummary.fetch_all()
		self.assertEqual(len(current_response_summary), len(old_response_summary) + 1)
	
	def test_update_response_summary(self):
		self.test_response_summary.save()
		response_summary = ResponseSummary.get(self.test_response_summary.id)
		old_response_summary_status = response_summary.status
		response_summary.status = 'failed'
		response_summary.save()
		new_response_status = ResponseSummary.get(self.test_response_summary.id)
		self.assertEqual(new_response_status.status, 'failed')
		self.assertNotEqual(old_response_summary_status, new_response_status)
	
	def test_delete_response_summary(self):
		self.test_response_summary.save()
		old_response_summarys = ResponseSummary.fetch_all()
		particular_response = ResponseSummary.find_first(id=self.test_response_summary.id)
		particular_response.delete()
		current_response_summarys = ResponseSummary.fetch_all()
		self.assertNotEqual(len(old_response_summarys), len(current_response_summarys))
		self.assertEqual(len(current_response_summarys), 0)

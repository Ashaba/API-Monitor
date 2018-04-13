from test.base import BaseTestCase
from application.models import Header


class TestHeaderModel(BaseTestCase):

	def setUp(self):
		super(TestHeaderModel, self).setUp()
		self.test_header = Header(
			request_id="1",
			key="Authorization",
			value="ey5TKcv7812230mPReaT"
		)

	def test_create_header(self):
		old_headers = Header.fetch_all()
		self.assertEqual(len(old_headers), 0)
		self.test_header.save()
		current_headers = Header.fetch_all()
		self.assertEqual(len(current_headers), len(old_headers) + 1)
	
	def test_update_header(self):
		self.test_header.save()
		header = Header.get(self.test_header.id)
		old_header_key = header.key
		header.key = 'Token'
		header.save()
		new_header_key = Header.get(self.test_header.id)
		self.assertEqual(new_header_key.key, 'Token')
		self.assertNotEqual(old_header_key, new_header_key)
	
	def test_delete_header(self):
		self.test_header.save()
		old_headers = Header.fetch_all()
		particular_header = Header.find_first(id=self.test_header.id)
		particular_header.delete()
		current_headers = Header.fetch_all()
		self.assertNotEqual(len(old_headers), len(current_headers))
		self.assertEqual(len(current_headers), 0)

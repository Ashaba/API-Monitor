from test.base import BaseTestCase
from application.auth.models import User


class TestUser(BaseTestCase):
	test_user = User(
		name="Test User",
		email="test.user@andela.com",
		image_url="test-image.jpg"
	)
	
	test_user2 = User(
		name="Test User2",
		email="test.user2@andela.com",
		image_url="test-image2.jpg"
	)
	
	test_user3 = User(
		name="Test User3",
		email="test.user3@andela.com",
		image_url="test-image3.jpg"
	)
	
	def test_create_user(self):
		old_users = User.fetch_all()
		self.test_user.save()
		new_users = User.fetch_all()
		self.assertEqual(len(new_users), len(old_users)+1)
		
	def test_update_user(self):
		self.test_user2.save()
		user = User.get(self.test_user.id)
		old_name = user.name
		user.name = "API Monitor Test"
		user.save()
		current_user = User.get(self.test_user.id)
		new_user_name = current_user.name
		self.assertEqual(new_user_name, "API Monitor Test")
		self.assertNotEqual(old_name, new_user_name)
		
	def test_delete_user(self):
		self.test_user3.save()
		old_users = User.fetch_all()
		particular_user = User.find_first(email=self.test_user3.email)
		particular_user.delete()
		current_users = User.fetch_all()
		self.assertNotEqual(len(old_users), len(current_users))
		self.assertEqual(len(current_users), 0)

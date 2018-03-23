from ..base import BaseTestCase, db
from application.models import Collection, Team
from application.auth.models import User


class TestCollectionModel(BaseTestCase):
	test_user = User(
		name="Test User",
		email="test.user@andela.com",
		image_url="test-image.jpg"
	)
	
	def test_create_collection(self):
		""" Test creation of a collection using the foreign keys of User and Team"""
		self.test_user.save()
		team = Team(
			name="Monitor Collection",
			user_id=self.test_user.id
		)
		team.save()
		collection = Collection(
			name="Test Collection",
			user_id=self.test_user.id,
			team_id=team.id
		)
		old_collection = Collection.fetch_all()
		self.assertEqual(len(old_collection), 0)
		collection.save()
		current_collection = Collection.fetch_all()
		self.assertEqual(len(current_collection), len(old_collection) + 1)
		
	def test_update_collection(self):
		collection = Collection(
			name="Test Collection",
			user_id="1",
			team_id="1"
		)
		collection.save()
		collection = Collection.get(collection.id)
		old_collection_name = collection.name
		collection.name = "New Test Collection Name"
		collection.save()
		current_collection = Collection.get(collection.id)
		self.assertEqual(current_collection.name, "New Test Collection Name")
		self.assertNotEqual(old_collection_name, current_collection.name)
		
	def test_delete_collection(self):
		collection = Collection(
			name="Test Collection",
			user_id="1",
			team_id="1"
		)
		collection.save()
		old_collections = Collection.fetch_all()
		particular_collection = Collection.find_first(id=collection.id)
		particular_collection.delete()
		current_collections = Collection.fetch_all()
		self.assertNotEqual(len(old_collections), len(current_collections))
		self.assertEqual(len(current_collections), 0)


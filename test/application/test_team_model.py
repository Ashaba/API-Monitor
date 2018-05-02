from test.base import BaseTestCase
from application.models import Team
from application.auth.models import User


class TestTeamModel(BaseTestCase):
	test_user = User(
		name="Test User",
		email="test.user@andela.com",
		image_url="test-image.jpg"
	)
	
	def test_create_team(self):
		"""Test the creation of a team with the use of a User foreign key"""
		self.test_user.save()
		team = Team(
			name="Monitor Collection",
			user_id=self.test_user.id
		)
		old_team = Team.fetch_all()
		self.assertEqual(len(old_team), 0)
		team.save()
		current_team = Team.fetch_all()
		self.assertEqual(len(current_team), len(old_team)+1)
	
	def test_update_team(self):
		self.test_user.save()
		team = Team(
			name="Monitor Collection",
			user_id="1"
		)
		team.save()
		team = Team.get(team.id)
		old_team_name = team.name
		team.name = "CALM API TEAM"
		team.save()
		new_team = Team.get(team.id)
		self.assertEqual(new_team.name, "CALM API TEAM")
		self.assertNotEqual(old_team_name, new_team)
		
	def test_delete_team(self):
		team = Team(
			name="Monitor Collection",
			user_id="1"
		)
		team.save()
		old_teams = Team.fetch_all()
		particular_team = Team.find_first(id=team.id)
		particular_team.delete()
		current_teams = Team.fetch_all()
		self.assertNotEqual(len(old_teams), len(current_teams))
		self.assertEqual(len(current_teams), 0)

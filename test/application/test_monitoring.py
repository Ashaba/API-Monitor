import os
import redis
from test.base import BaseTestCase
from application.monitoring_tasks import monitoring_checks


class TestMonitoring(BaseTestCase):
	def test_redis_server(self):
		url = os.environ.get("REDIS_URL") or "redis://localhost:6379"
		redis_connection = redis.StrictRedis.from_url(url=url)
		self.assertTrue(redis_connection)
		
	def test_monitoring_checks_with_no_data(self):
		monitoring = monitoring_checks()
		self.assertIsNone(monitoring)


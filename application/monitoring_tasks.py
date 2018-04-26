import os
import redis
import logging
from celery.task.base import periodic_task
from datetime import timedelta
import time
from main import celery

from application.models import Collection
from application.helpers import run_collection_checks

logger = logging.getLogger(__name__)


url = os.environ.get("REDIS_URL") or "redis://localhost:6379"
REDIS_CONN = redis.StrictRedis.from_url(url=url)


try:
    REDIS_CONN.ping()
    logger.info("Redis is connected!")
except redis.ConnectionError:
    logger.error("Redis connection error!")


@celery.task(name='tasks.async_monitoring_checks')
def monitoring_checks():
    logger.info("Running Monitoring checks")
    try:
        collections = Collection.fetch_all()
        scheduled_collections = [y for y in collections if y.interval]
        for collection in scheduled_collections:
            time.sleep(collection.interval)
            run_collection_checks(collection.id, collection.interval)
    except Exception as e:
        logger.error(e)


def async_monitoring_checks():
    """ Asynchronous task, called from API endpoint. """
    monitoring_checks.delay()
    return


@periodic_task(run_every=timedelta(seconds=60))
def periodic_monitoring_checks():
    return monitoring_checks()

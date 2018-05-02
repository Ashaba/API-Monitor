import time
import logging
from threading import Thread, Lock
from queue import Queue
from application.models import Collection
from application.helpers import run_collection_checks

logger = logging.getLogger(__name__)

thread_lock = Lock()


class RequestWorker(Thread):
	def __init__(self, name, counter, queue):
		Thread.__init__(self)
		self.name = name
		self.counter = counter
		self.queue = queue
		
	def run(self):
		logger.info("Starting " + self.name)
		thread_lock.acquire()
		collection_id, interval = self.queue.get()
		# time.sleep(interval)
		run_collection_checks(collection_id, interval)
		thread_lock.release()
		

def checks_runner(app_context):
	ts = time.time()
	queue = Queue()
	threads = []
	while True:
		with app_context:
			collections = Collection.fetch_all()
		thread_list = [y for y in collections if y.interval]
		for collection in thread_list:
			time.sleep(collection.interval)
			worker = RequestWorker(collection.name, len(thread_list), queue)
			worker.daemon = True
			worker.start()
			threads.append(worker)
			logger.info('Queueing {}'.format(collection.name))
			queue.put((collection.id, collection.interval))
		queue.join()
		logger.info('Took {}'.format(time.time() - ts))


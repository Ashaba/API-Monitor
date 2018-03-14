import requests
from application.models import Request


def run_collection_checks(collection_id):
	requests = Request.filter_by(collection_id=collection_id)
	for req in requests:
		print(req)


def make_get_request(url, headers=None):
	request = requests.get(url, headers=headers)
	response = {
		"statusCode": request.status_code,
		"content": request.content,
		"data": request.json(),
		"url": request.url,
		"headers": request.headers
	}
	return response

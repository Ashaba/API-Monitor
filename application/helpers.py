import requests, json
from application.models import Request


def run_collection_checks(collection_id):
	check_requests = Request.filter_by(collection_id=collection_id)
	response = []
	for req in check_requests:
		headers = req.headers
		url = req.url
		if req.method == "GET":
			if req.headers == "{}":
				headers = None
			response.append(make_get_request(url, headers))
	return response


def make_get_request(url, headers=None):
	request = requests.get(url, headers=headers)
	try:
		response_object = request.json()
	except Exception:
		response_object = request.content.decode("utf-8")
		
	response = {
		"status_code": request.status_code,
		"data": response_object,
		"url": request.url,
		"headers": json.dumps(dict(request.headers)),
		"response_time": request.elapsed.total_seconds()
	}
	return response

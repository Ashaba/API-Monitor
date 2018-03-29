import requests
import json
import re
from application.models import Request


def valid_url(url):
	pattern = re.compile(
		r'^(?:http|ftp)s?://'  # http:// or https://
		r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
		r'localhost|'  # localhost...
		r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
		r'(?::\d+)?'  # optional port
		r'(?:/?|[/?]\S+)$', re.IGNORECASE)
	if pattern.match(url):
		return True
	else:
		return False
	

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
	if valid_url(url):
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
	response = {
		"status": "fail",
		"message": "invalid url"
	}
	return response


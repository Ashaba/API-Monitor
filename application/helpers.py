import requests
import json
import re
from application.models import Request, Response, ResponseSummary, ResponseAssertion, Collection
from application.models import Request, Collection


def collection_scheduler(app_context):
	with app_context:
		collections = Collection.fetch_all()
		for collection in collections:
			if collection.interval:
				run_collection_checks(collection.id, collection.interval)


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
	

def run_collection_checks(collection_id, run_from):
	checks = Request.filter_by(collection_id=collection_id)
	response_summary = ResponseSummary(
		status='success',
		failures=0,
		run_from=run_from,
		collection_id=collection_id
	)

	for check in checks:
		headers = {}
		for header in check.headers:
			headers[header.key] = header.value

		if check.method == "GET":
			result = requests.get(check.url, headers=headers, verify=False)
		response = Response(
			status_code=result.status_code,
			response_time=int(result.elapsed.total_seconds()),
			headers=json.dumps(dict(result.headers)),
			status='success',
			failures=0,
			request_id=check.id,
			response_summary_id=response_summary.id
		)
		try:
			data = json.dumps(result.json())
		except json.decoder.JSONDecodeError:
			data = str(result.content)
		response.data = data

		for assertion in check.assertions:
			response_assertion = ResponseAssertion(
				assertion_type=assertion.assertion_type,
				comparison=assertion.comparison,
				value=assertion.value,
				status='failed',
				request_assertion_id=assertion.id,
				response_id=response.id)
			if assertion.assertion_type == 'Status Code':
				if assertion.value == response.status_code:
					response_assertion.status = "success"
			else:
				if 'less' in assertion.comparison:
					if response.response_time <= assertion.value:
						response_assertion.status = "success"
				else:
					if response.response_time >= assertion.value:
						response_assertion.status = "success"
			if response_assertion.status == 'failed':
				response.failures += 1
				response.status = 'failed'
			response.response_assertions.append(response_assertion)
	
		if response.status == 'failed':
			response_summary.failures += 1
			response_summary.status = 'failed'
		response_summary.responses.append(response)

	response_summary.save()


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

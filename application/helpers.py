import requests
import json
import re
import logging
from flask import current_app
from flask_mail import Mail, Message
from application.models import Response, ResponseSummary, ResponseAssertion
from application.models import Request, Collection, Team
from application.auth.models import User


logger = logging.getLogger(__name__)


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
	request_check = Request.filter_by(collection_id=collection_id)
	response_summary = ResponseSummary(
		run_from=run_from,
		collection_id=collection_id
	)
	collection_status = "success"
	for req in request_check:
		headers = {}
		for header in req.headers:
			headers[header.key] = header.value
		response = make_request(req.url, req.method, headers=headers)
		response.request_id = req.id
		response.response_summary_id = response_summary.id
		
		failures, status = test_assertions(response, req)
		if status == "success":
			collection_status = "success"
		else:
			collection_status = "failed"
		response_summary.failures = failures
		response_summary.status = status
		response_summary.responses.append(response)
	if collection_status == "failed":
		mail = Mail(current_app)
		collection = Collection.get(collection_id)
		team = Team.get(collection.team_id)
		user = User.get(team.user_id)
		msg = Message(
			"Failed check: "+collection.name, sender="john.ashabahebwa@andela.com", recipients=[user.email],
			body=collection.name+" Has failing checks")
		Message()
		mail.send(msg)
		
	response_summary.save()


def make_request(url, method, headers=None):
	try:
		request = requests.get(url, headers=headers, verify=False)
		try:
			response_object = request.json()
		except Exception:
			response_object = request.content.decode("utf-8")
		
		response = Response(
			status_code=request.status_code,
			response_time=int(request.elapsed.total_seconds()),
			headers=json.dumps(dict(request.headers)),
			data=response_object,
		)
		return response

	except Exception as e:
		logger.error(e)
		return None


def test_assertions(response, req):
	failures = 0
	status = "success"
	for assertion in req.assertions:
		response_assertion = ResponseAssertion(
			assertion_type=assertion.assertion_type,
			comparison=assertion.comparison,
			value=assertion.value,
			request_assertion_id=assertion.id,
			response_id=response.id)
		
		if 'less' in assertion.comparison:
			if response.response_time <= assertion.value:
				response_assertion.status = status
			else:
				failures += 1
				status = "failed"
		
		if assertion.assertion_type == 'Status Code':
			if assertion.value == response.status_code:
				response_assertion.status = status
			else:
				failures += 1
				status = "failed"
		response.failures = failures
		response.status = status
		response.response_assertions.append(response_assertion)
		response.save()
	
	return failures, status


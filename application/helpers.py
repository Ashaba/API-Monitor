import requests


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

from flask import Blueprint, render_template, request, jsonify

from application.auth.helpers import (current_user, authentication_required)
from application.models import Team, Collection, RequestAssertion, ResponseSummary, Request, Header
from application.helpers import run_collection_checks

app_view = Blueprint('app_view', __name__, template_folder='templates')


@app_view.route('/dashboard', methods=['POST', 'GET'])
@authentication_required
def dashboard():
    context = dict()
    context["title"] = "Dashboard"
    if request.method == 'POST':
        payload = request.get_json()
        def handle_request(n):
            if n < 1:
                return "no data"
            else:
                n -= 1
                req = Request(
                    collection_id=2,
                    method=payload[n].get("method"),
                    body=payload[n].get("body"),
                    url=payload[n].get("url"),
                    headers=payload[n].get("headers")
                )
                req.save()
                return handle_request(n)
        return handle_request(len(payload))

    return render_template("dashboard.html", context=context)


@app_view.route('/team', methods=['POST', 'GET'])
@authentication_required
def team():
    context = dict()
    context["title"] = "Team"
    if request.method == 'POST':
        team = Team(name=request.form["team"], user_id=current_user().id)
        team.save()
    return render_template("team.html", context=context)


@app_view.route('/collections', methods=['POST', 'GET', 'DELETE'])
@authentication_required
def collections():
    context = dict()
    context["teams"] = Team.fetch_all()
    context["title"] = "Collections"
    if request.method == 'POST':
        name = request.form["collection"]
        team_id = request.form["team"] if request.form["team"] != 'none' else None 

        existing_collection = Collection.query.filter(Collection.user_id == current_user().id,
                                                      Collection.name == name).first()
        if existing_collection:
            return "duplicate_collection"

        collection = Collection(name=name, user_id=current_user().id, team_id=team_id)
        collection.save()

    elif request.method == 'DELETE':
        collection_id = request.args.get('id', '0')
        collection = Collection.get(collection_id)
        collection.delete()
    
    user_collections = Collection.filter_all(user_id=current_user().id)
    context["collections"] = user_collections
    return render_template('collections.html', context=context)


@app_view.route('/collection-details/<collection_id>', methods=['GET', 'PUT'])
@authentication_required
def collection_details(collection_id=None):
    context = {}
    requests = Request.filter_by(collection_id=collection_id)
    checks = []
    for req in requests:
        reqDetails = {}
        reqDetails['id'] = req.id
        reqDetails['method'] = req.method
        reqDetails['url'] = req.url
        headers = []
        for h in req.headers:
            header = h.serialize()
            headers.append(header)
        reqDetails['headers'] = headers
        assertions = []
        for ass in req.assertions:
            assertion = ass.serialize()
            assertions.append(assertion)
        reqDetails['assertions'] = assertions
        checks.append(reqDetails)
    context['checks'] = checks

    response_summaries = ResponseSummary.filter_by(collection_id=collection_id)
    results = []
    for response_summary in response_summaries:
        responseSet = {}
        summary = response_summary.serialize()
        summary['date_created'] = response_summary.date_created.strftime('%b %d %RHrs')
        responses = []
        for res in response_summary.responses:
            response = res.serialize()
            response['url'] = res.request.url
            response['method'] = res.request.method
            response['assertions'] = []
            for _assertion in res.response_assertions:
                assertion = _assertion.serialize()
                if _assertion.assertion_type == 'Status Code':
                    assertion['received'] = res.status_code
                else:
                    assertion['received'] = str(res.response_time) + 'ms'
                    assertion['value'] = str(assertion['value']) + 'ms'
                response['assertions'].append(assertion)
            responses.append(response)
        responseSet['summary'] = summary
        responseSet['results'] = responses
        results.append(responseSet)
    context['results'] = results
    context['collection_name'] = Collection.get(collection_id).name
    collection = Collection.get(collection_id)
    context["collection"] = collection.serialize()
    
    return render_template('collection_details.html', context=context)


@app_view.route('/collection-details/<collection_id>/<run_from>/run-checks', methods=['GET'])
@authentication_required
def collection_checks(collection_id=None, run_from='Schedule'):
    run_collection_checks(collection_id, run_from)
    response = jsonify(dict(
        status="success"
    ))
    return response


@app_view.route('/collection-details/<collection_id>/update', methods=['POST'])
@authentication_required
def update_collection_checks(collection_id=None):
    checks = request.get_json()
    errors = []
    checkIndex = 0
    for _check in checks:
        checkIndex += 1
        error = dict(
            checkIndex=checkIndex
        )
        if _check['id'] == '':
            check = Request.filter_by(
                url=_check['url'], method=_check['method'], collection_id=collection_id).first()
            if check is None:
                check = Request()
            else:
                error['message'] = 'Duplicate url'
                error['selector'] = '#checksFormContainer div.check:nth-child(' + str(checkIndex) + ') [name="url"]'
                errors.append(error)
                continue
        else:
            check = Request.get(_check['id'])
        check.method = _check['method']
        check.url = _check['url']
        check.collection_id = collection_id
        check.save()

        header_index = 0
        for _header in _check['headers']:
            header_index += 1
            if _header['id'] == '':
                header = Header.filter_by(
                    key=_header['key'], request_id=check.id).first()
                if header is None:
                    header = Header()
                else:
                    error['message'] = 'Duplicate header key'
                    error['selector'] = '#' + str(check.id) + '.check .headers div:nth-child(' + str(header_index) + ') [name="headerKey"]'
                    errors.append(error)
                    continue
            else:
                header = Header.get(_header['id'])
            header.key = _header['key']
            header.value = _header['value']
            header.request_id = check.id
            header.save()
        assertion_index = 1
        for _assertion in _check['assertions']:
            assertion_index += 1
            if _assertion['id'] == '':
                assertion = RequestAssertion.filter_by(
                    assertion_type=_assertion['assertion_type'],
                    comparison=_assertion['comparison'],
                    request_id=check.id).first()
                if assertion is None:
                    assertion = RequestAssertion()
                else:
                    error['message'] = 'Duplicate assertion',
                    error['selector'] = '#' + str(check.id) + '.check .assertions div:nth-child(' + str(assertion_index) + ') [name="assertionSource"]'
                    errors.append(error)
                    continue
            else:
                assertion = RequestAssertion.get(_assertion['id'])
            assertion.assertion_type = _assertion['assertion_type']
            assertion.comparison = _assertion['comparison']
            assertion.value = _assertion['value']
            assertion.request_id = check.id
            assertion.save()
    response = jsonify(dict(
        errors=errors
    ))
    return response

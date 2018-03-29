from flask import Blueprint, render_template, request, jsonify

from application.auth.helpers import (current_user, authentication_required)
from application.models import Team, Collection, Request
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


@app_view.route('/results/<collection_id>', methods=['GET'])
@app_view.route('/results', methods=['GET'])
@authentication_required
def result(collection_id=None):
    response = jsonify(dict(
        status="success",
        response=run_collection_checks(collection_id)
    ))
    response.status_code = 200
    return response


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


@app_view.route('/collection_details', methods=['GET'])
@authentication_required
def results():
    context = dict()
    context["title"] = "Results"
    context["checks"] = [
        {
            'id': '123',
            'method': 'GET',
            'url': 'facebook.com/login',
            'headers': [
                {
                    'id': '9883',
                    'key': 'token',
                    'value': '67sqqq8jbsbakbakbs'
                },
                {
                    'id': '746',
                    'key': 'userId',
                    'value': 'flyguy'
                }
            ],
            'assertions': [
                {
                    'id': '211',
                    'type': 'Status Code',
                    'comparison': 'equal (number)',
                    'value': '200',
                },
                {
                    'id': '212',
                    'type': 'Response Time (ms)',
                    'comparison': 'greater than or equal to',
                    'value': '100ms',
                },
            ]
        },
        {
            'id': '124',
            'method': 'POST',
            'url': 'yahoo.com/login',
            'headers': [
                {
                    'id': '45',
                    'key': 'userID',
                    'value': '7801'
                },
                {
                    'id': '14',
                    'key': 'userEmail',
                    'value': 'test@yahoo.com'
                }
            ],
            'assertions': [
                {
                    'id': '90',
                    'type': 'Status Code',
                    'comparison': 'equal (number)',
                    'value': '201',
                },
                {
                    'id': '21',
                    'type': 'Response Time (ms)',
                    'comparison': 'greater than or equal to',
                    'value': '100ms',
                },
            ]
        },
        {
            'id': '125',
            'method': 'PUT',
            'url': 'calm-staging.andela.com/stacks',
            'headers': [
                {
                    'id': '71',
                    'key': 'stackID',
                    'value': '67eyT'
                },
                {
                    'id': '73',
                    'key': 'Token',
                    'value': '783NTmmzaq&TG33cBgASKy'
                }
            ],
            'assertions': [
                {
                    'id': '2118',
                    'type': 'Status Code',
                    'comparison': 'equal (number)',
                    'value': '200',
                },
                {
                    'id': '222',
                    'type': 'Response Time (ms)',
                    'comparison': 'less than',
                    'value': '300ms',
                },
            ]
        },
    ]
    context['results'] = [
        {
            'summary': {
                'status': 'success',
                'failures': '0',
                'date': 'Mar 15 6:17pm',
                'runFrom': 'Dashboard'
            },
            'results': [
                {
                    'id': '123',
                    'url': 'facebook.com/login',
                    'method': 'GET/',
                    'statusCode': '200',
                    'responseTime': '500ms',
                    'checkId': '124',
                    'assertions': [
                        {
                            'id': '211',
                            'type': 'Status code',
                            'comparison': 'equal to',
                            'status': 'success',
                            'expected': '200',
                            'received': '200'
                        },
                        {
                            'id': '212',
                            'type': 'Response time',
                            'comparison': 'less than',
                            'status': 'fail',
                            'expected': '100ms',
                            'received': '500ms'
                        },
                    ]
                },
                {
                    'id': '123',
                    'url': 'facebook.com/login',
                    'method': 'POST/',
                    'statusCode': '200',
                    'responseTime': '723ms',
                    'checkId': '123',
                    'assertions': [
                        {
                            'id': '211',
                            'type': 'Status code',
                            'comparison': 'equal to',
                            'status': 'success',
                            'expected': '200',
                            'received': '200'
                        },
                        {
                            'id': '212',
                            'type': 'Response time',
                            'comparison': 'less than',
                            'status': 'fail',
                            'expected': '100ms',
                            'received': '500ms'
                        },
                    ]
                },
                {
                    'id': '123',
                    'url': 'facebook.com/login',
                    'method': 'POST/',
                    'statusCode': '200',
                    'responseTime': '723ms',
                    'checkId': '125',
                    'assertions': [
                        {
                            'id': '211',
                            'type': 'Status code',
                            'comparison': 'equal to',
                            'status': 'success',
                            'expected': '200',
                            'received': '200'
                        },
                        {
                            'id': '212',
                            'type': 'Response time',
                            'comparison': 'less than',
                            'status': 'fail',
                            'expected': '100ms',
                            'received': '500ms'
                        },
                    ]
                },
                {
                    'id': '123',
                    'url': 'facebook.com/login',
                    'method': 'POST/',
                    'statusCode': '200',
                    'responseTime': '723ms',
                    'checkId': '124',
                    'assertions': [
                        {
                            'id': '211',
                            'type': 'Status code',
                            'comparison': 'equal to',
                            'status': 'success',
                            'expected': '200',
                            'received': '200'
                        },
                        {
                            'id': '212',
                            'type': 'Response time',
                            'comparison': 'less than',
                            'status': 'fail',
                            'expected': '100ms',
                            'received': '500ms'
                        },
                    ]
                },
                {
                    'id': '123',
                    'url': 'facebook.com/login',
                    'method': 'POST/',
                    'statusCode': '200',
                    'responseTime': '723ms',
                    'checkId': '123',
                    'assertions': [
                        {
                            'id': '211',
                            'type': 'Status code',
                            'comparison': 'equal to',
                            'status': 'success',
                            'expected': '200',
                            'received': '200'
                        },
                        {
                            'id': '212',
                            'type': 'Response time',
                            'comparison': 'less than',
                            'status': 'fail',
                            'expected': '100ms',
                            'received': '500ms'
                        },
                    ]
                }
            ]
        },
        {
            'summary': {
                'status': 'failed',
                'failures': '1',
                'date': 'Jun 26 16:35pm',
                'runFrom': 'Schedule'
            },
            'results': [
                {
                    'id': '123',
                    'url': 'facebook.com/login',
                    'method': 'GET/',
                    'statusCode': '200',
                    'responseTime': '500ms',
                    'checkId': '123',
                    'assertions': [
                        {
                            'id': '211',
                            'type': 'Status code',
                            'comparison': 'equal to',
                            'status': 'success',
                            'expected': '200',
                            'received': '200'
                        },
                        {
                            'id': '212',
                            'type': 'Response time',
                            'comparison': 'less than',
                            'status': 'fail',
                            'expected': '100ms',
                            'received': '500ms'
                        },
                    ]
                },
                {
                    'id': '123',
                    'url': 'facebook.com/login',
                    'method': 'POST/',
                    'statusCode': '200',
                    'responseTime': '723ms',
                    'checkId': '124',
                    'assertions': [
                        {
                            'id': '211',
                            'type': 'Status code',
                            'comparison': 'equal to',
                            'status': 'success',
                            'expected': '200',
                            'received': '200'
                        },
                        {
                            'id': '212',
                            'type': 'Response time',
                            'comparison': 'less than',
                            'status': 'fail',
                            'expected': '100ms',
                            'received': '500ms'
                        },
                    ]
                }
            ]
        },
        {
            'summary': {
                'status': 'failed',
                'failures': '22',
                'date': 'Feb 30 12:00pm',
                'runFrom': 'Dashboard'
            },
            'results': [
                {
                    'id': '123',
                    'url': 'facebook.com/login',
                    'method': 'POST/',
                    'statusCode': '200',
                    'responseTime': '723ms',
                    'checkId': '125',
                    'assertions': [
                        {
                            'id': '211',
                            'type': 'Status code',
                            'comparison': 'equal to',
                            'status': 'success',
                            'expected': '200',
                            'received': '200'
                        },
                        {
                            'id': '212',
                            'type': 'Response time',
                            'comparison': 'less than',
                            'status': 'fail',
                            'expected': '100ms',
                            'received': '500ms'
                        },
                    ]
                },
                {
                    'id': '123',
                    'url': 'facebook.com/login',
                    'method': 'POST/',
                    'statusCode': '200',
                    'responseTime': '723ms',
                    'checkId': '123',
                    'assertions': [
                        {
                            'id': '211',
                            'type': 'Status code',
                            'comparison': 'equal to',
                            'status': 'success',
                            'expected': '200',
                            'received': '200'
                        },
                        {
                            'id': '212',
                            'type': 'Response time',
                            'comparison': 'less than',
                            'status': 'fail',
                            'expected': '100ms',
                            'received': '500ms'
                        },
                    ]
                },
                {
                    'id': '123',
                    'url': 'facebook.com/login',
                    'method': 'POST/',
                    'statusCode': '200',
                    'responseTime': '723ms',
                    'checkId': '124',
                    'assertions': [
                        {
                            'id': '211',
                            'type': 'Status code',
                            'comparison': 'equal to',
                            'status': 'success',
                            'expected': '200',
                            'received': '200'
                        },
                        {
                            'id': '212',
                            'type': 'Response time',
                            'comparison': 'less than',
                            'status': 'fail',
                            'expected': '100ms',
                            'received': '500ms'
                        },
                    ]
                }
            ]
        }
        
    ]
    return render_template('collection_details.html', context=context)

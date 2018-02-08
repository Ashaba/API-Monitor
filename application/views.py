from flask import Blueprint, render_template, request, jsonify
import requests

from application.auth.helpers import (current_user)
from application.models import Team, Collection

app_view = Blueprint('app_view', __name__, template_folder='templates')


@app_view.route('/dashboard', methods=['POST', 'GET'])
def dashboard():
    context = dict()
    context["title"] = "Dashboard"
    if request.method == 'POST':
        payload = request.get_json()
        if payload:
            if payload['method'] == 'get':
                response = requests.get(payload['url'], headers=payload['headers'])
                values = []
                data = {
                    "statusCode": response.status_code,
                    "body": response.content.decode("utf-8"),
                    "url": response.url,
                }
                values.append(data)
                return jsonify(dict(status="success", data=data))
    return render_template("dashboard.html", context=context)


@app_view.route('/team', methods=['POST', 'GET'])
def team():
    context = dict()
    context["title"] = "Team"
    if request.method == 'POST':
        team = Team(name=request.form["team"], user_id=current_user().id)
        team.save()
    return render_template("team.html", context=context)


@app_view.route('/collections', methods=['POST', 'GET'])
def collections():
    context = dict()
    context["teams"] = Team.fetch_all()
    context["title"] = "Collections"
    if request.method == 'POST':
        name = request.form["collection"]
        team_id = request.form["team"]
        collection = Collection(name=name, user_id=current_user().id, team_id=team_id)
        collection.save()
    return render_template('collections.html', context=context)


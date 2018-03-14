from flask import Blueprint, render_template, request, jsonify

from application.auth.helpers import (current_user, authentication_required)
from application.models import Team, Collection, Request
from application.helpers import (run_collection_checks)

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
                    headers=payload[n].get("headerKeys")
                )
                req.save()
                # collection = payload[n].get("collection")
                run_collection_checks(2)
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


@app_view.route('/collections', methods=['POST', 'GET'])
@authentication_required
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

from flask import Blueprint, render_template , request, jsonify
from flask_login import login_required, current_user
from . import db 
from .models import Activities, Saletaxes

main = Blueprint('main', __name__)

@main.route('/')
def index():
  return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
  return render_template('profile.html', username = current_user.username)

@main.route("/activities", methods=["GET"])
@login_required
def handle_activities():

    if request.method == "GET":
        allActivities = Activities.query.all()

        if not allActivities:
            return jsonify({"msg": "Activities not found"}), 404

        return jsonify([x.serialize() for x in allActivities]), 200

    return "Invalid Method", 404


@main.route("/activitiesbycategory", methods=["POST"])
@login_required
def handle_activities_by_category():
    body = request.get_json()

    if request.method == "POST":
        GetAllActivitiesByCategory = Activities.query.filter_by(
            cat=body["category"]
        ).all()

        if not GetAllActivitiesByCategory:
            return jsonify({"msg": "Activities not found"}), 404

        return jsonify([x.serialize() for x in GetAllActivitiesByCategory]), 200

    return "Invalid Method", 404


@main.route("/saletaxes", methods=["GET"])
@login_required
def handle_saletaxes():

    if request.method == "GET":
        allSaletaxes = Saletaxes.query.all()

        if not allSaletaxes:
            return jsonify({"msg": "Sale Taxes not found"}), 404

        return jsonify([x.serialize() for x in allSaletaxes]), 200

    return "Invalid Method", 404


@main.route("/saletaxesbystate", methods=["POST"])
@login_required
def handle_saletaxes_by_state():
    body = request.get_json()

    if request.method == "POST":
        GetTaxByState = Saletaxes.query.filter_by(state=body["state"]).first()

        if not GetTaxByState:
            return jsonify({"msg": "Sale Taxes not found for this state"}), 404

        # return jsonify( [x.serialize() for x in GetTaxByState] ), 200
        return jsonify(GetTaxByState.rate), 200

    return "Invalid Method", 404
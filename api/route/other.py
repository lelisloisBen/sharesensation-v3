import jwt
import datetime
from urllib import response
import flask
import flask_restx
from api import api
from api.schema.User import UserSchema
from api.utils.mail import send_verify_email, valid_email_format
from database import db
from flask import request, Response, current_app as app, jsonify
from flask_login import login_user, logout_user
from flask_restx import Resource
from database.model.User import User
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
from database.model.Activity import Activity
from database.model.SaleTax import SaleTax
import logging

logger = logging.getLogger(__name__)

@app.route('/activities', methods=['GET'])
def handle_activities():
    logger.info("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

    if request.method == 'GET':
        allActivities = Activity.query.all()

        if not allActivities:
            return jsonify({'msg':'Activities not found'}), 404

        return jsonify( [x.serialize() for x in allActivities] ), 200

    return "Invalid Method", 404

@app.route('/activitiesbycategory', methods=['POST'])
def handle_activities_by_category():
    body = request.get_json()

    if request.method == 'POST':
        GetAllActivitiesByCategory = Activity.query.filter_by(cat=body['category']).all()

        if not GetAllActivitiesByCategory:
            return jsonify({'msg':'Activities not found'}), 404

        return jsonify( [x.serialize() for x in GetAllActivitiesByCategory] ), 200

    return "Invalid Method", 404

@app.route('/saletaxes', methods=['GET'])
def handle_saletaxes():

    if request.method == 'GET':
        allSaletaxes = SaleTax.query.all()

        if not allSaletaxes:
            return jsonify({'msg':'Sale Taxes not found'}), 404

        return jsonify( [x.serialize() for x in allSaletaxes] ), 200

    return "Invalid Method", 404

@app.route('/saletaxesbystate', methods=['POST'])
def handle_saletaxes_by_state():
    body = request.get_json()
    
    if request.method == 'POST':
        GetTaxByState = SaleTax.query.filter_by(state=body['state']).first()

        if not GetTaxByState:
            return jsonify({'msg':'Sale Taxes not found for this state'}), 404

        # return jsonify( [x.serialize() for x in GetTaxByState] ), 200
        return jsonify( GetTaxByState.rate ), 200

    return "Invalid Method", 404
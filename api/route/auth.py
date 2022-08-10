from api import api
from flask_restx import Resource
import flask_restx
from flask import request
from api.exception import APIException
from api.utils.mail import valid_email_format
from werkzeug.security import generate_password_hash
from database import db
import flask
from api.utils.mail import send_verify_email

auth_ns = api.namespace('auth', validate=True)

signup_model = auth_ns.model(
    "User Signup",
    {
        "firstname": flask_restx.fields.String(required=True),
        "lastname": flask_restx.fields.String(required=True),
        "email": flask_restx.fields.String(required=True),
        "password": flask_restx.fields.String(required=True),
    },
)

@auth_ns.route("/signup")
class User(Resource):
    @auth_ns.doc(data=signup_model)
    def post(self, *args, **kwargs):
        """User Signup"""
        data = request.json

        if data is None:
            raise APIException("You need to specify the request data as a json object", status_code=400)
        if 'firstname' not in data and 'lastname' not in data:
            raise APIException("You need to specify the first name and last name", status_code=400)
        if 'password' not in data and 'email' not in data:
            raise APIException("You need to specify the password and email", status_code=400)
        if 'firstname' not in data:
            raise APIException('You need to specify the first name', status_code=400)
        if 'lastname' not in data:
            raise APIException('You need to specify the last name', status_code=400)
        if 'password' not in data:
            raise APIException('You need to specify the password', status_code=400)
        if 'email' not in data:
            raise APIException('You need to specify the email', status_code=400)

        # validate email
        if not valid_email_format(data["email"]):
            raise APIException('Email is not correct', status_code=400)

        try:
            new_user = User(firstname = data['firstname'], email = data['email'], password = generate_password_hash(data['password'], method='sha256'))
            send_verify_email(new_user)
            db.session.add(new_user)
            db.session.commit()
            return flask.make_response()
        except:
            raise APIException('Register failed', status_code=400)
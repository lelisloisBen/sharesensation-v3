import jwt
import datetime
from urllib import response
import flask
import flask_restx
from api import api
from api.schema.User import UserSchema
from api.utils.mail import send_verify_email, valid_email_format
from database import db
from flask import request, Response, current_app as app
from flask_login import login_user, logout_user
from flask_restx import Resource
from database.model.User import User
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps

auth_ns = api.namespace("auth", validate=True)

signup_model = auth_ns.model(
    "User Signup",
    {
        "firstname": flask_restx.fields.String(required=True),
        "lastname": flask_restx.fields.String(required=True),
        "email": flask_restx.fields.String(required=True),
        "password": flask_restx.fields.String(required=True),
    },
)

login_model = auth_ns.model(
    "User Login",
    {
        "email": flask_restx.fields.String(required=True),
        "password": flask_restx.fields.String(required=True),
    },
)

blacklist_token = set()

def token_required(f):
    """Verify if the token is valid."""
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'HTTP_AUTHORIZATION' in flask.request.headers.environ:
            token = flask.request.headers.environ['HTTP_AUTHORIZATION']
        if not token or token in blacklist_token:
            return flask.make_response('A valid token is missing.', 401)
        try:
            user_info = jwt.decode(token, app.config('SECRET_KEY'), algorithms=["HS256"])
            user = User.query.filter_by(email=user_info['email']).first()
        except:
            return flask.make_response('The token is invalid.', 401)
        return f(*args, **kwargs, user=user)
    return decorator


@auth_ns.route("/signup")
class AuthAPI(Resource):
    @auth_ns.doc(body=signup_model)
    def post(self, *args, **kwargs):
        """User Signup"""
        data = request.json

        if data is None:
            return "You need to specify the request data as a json object", 400
        if "firstname" not in data and "lastname" not in data:
            return "You need to specify the first name and last name", 400
        if "password" not in data and "email" not in data:
            return "You need to specify the password and email", 400
        if "firstname" not in data:
            return "You need to specify the first name", 400
        if "lastname" not in data:
            return "You need to specify the last name", 400
        if "password" not in data:
            return "You need to specify the password", 400
        if "email" not in data:
            return "You need to specify the email", 400

        # validate email
        if not valid_email_format(data["email"]):
            return "Email is not correct", 400

        try:
            new_user = User(
                firstname=data["firstname"],
                lastname=data["lastname"],
                email=data["email"],
                password=generate_password_hash(data["password"], method="sha256"),
            )
            db.session.add(new_user)
            db.session.commit()

            send_verify_email(new_user)
            return '{}', 200
        except:
            return "Register failed", 400


@auth_ns.route("/login")
class LoginUser(Resource):
    @auth_ns.doc(body=login_model)
    def post(self, *args, **kwargs):
        """Login User"""
        data = request.json

        user = User.query.filter_by(email=data.get("email", None)).first()
        if not user or not check_password_hash(
            user.password, data.get("password", None)
        ):
            return "User not found", 404

        if not user.confirmed:
            return "Email is not verified", 405

        exp = datetime.datetime.utcnow() + datetime.timedelta(days=1)
        token = jwt.encode({'email': user.email, 'exp': exp}, 
                            app.config['SECRET_KEY'], algorithm="HS256")

        resp = UserSchema().dump(user)
        resp['token'] = token
        return flask.jsonify(resp)


@auth_ns.route("/logout")
class LogoutUser(Resource):
    @token_required
    def post(self, *args, **kwargs):
        """Logout the user"""
        logout_user()
        return '{}', 200


@auth_ns.route('/confirm-email')
class ConfirmEmail(Resource):
    def post(self, *args, **kwargs):
        """Confirm verify email token"""
        data = request.json

        user = User.verify_email_token(data['token'])

        if not user:
            return "Token Error", 404

        user.confirmed = True
        user.confirmed_on = datetime.datetime.now()
        db.session.commit()

        return '', 200
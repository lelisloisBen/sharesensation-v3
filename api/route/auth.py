import flask
import flask_restx
from api import api
from api.exception import APIException
from api.schema.User import UserSchema
from api.utils.mail import send_verify_email, valid_email_format
from database import db
from flask import request
from flask_login import login_user, logout_user
from flask_restx import Resource
from werkzeug.security import check_password_hash, generate_password_hash

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


@auth_ns.route("/signup")
class User(Resource):
    @auth_ns.doc(data=signup_model)
    def post(self, *args, **kwargs):
        """User Signup"""
        data = request.json

        if data is None:
            raise APIException(
                "You need to specify the request data as a json object", status_code=400
            )
        if "firstname" not in data and "lastname" not in data:
            raise APIException(
                "You need to specify the first name and last name", status_code=400
            )
        if "password" not in data and "email" not in data:
            raise APIException(
                "You need to specify the password and email", status_code=400
            )
        if "firstname" not in data:
            raise APIException("You need to specify the first name", status_code=400)
        if "lastname" not in data:
            raise APIException("You need to specify the last name", status_code=400)
        if "password" not in data:
            raise APIException("You need to specify the password", status_code=400)
        if "email" not in data:
            raise APIException("You need to specify the email", status_code=400)

        # validate email
        if not valid_email_format(data["email"]):
            raise APIException("Email is not correct", status_code=400)

        try:
            new_user = User(
                firstname=data["firstname"],
                email=data["email"],
                password=generate_password_hash(data["password"], method="sha256"),
            )
            send_verify_email(new_user)
            db.session.add(new_user)
            db.session.commit()
            return flask.make_response()
        except:
            raise APIException("Register failed", status_code=400)


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

        login_user(user)

        return flask.jsonify(UserSchema().dump(user))


@auth_ns.route("/logout")
class LogoutUser(Resource):
    def post(self, *args, **kwargs):
        """Logout the user"""
        logout_user()
        return flask.make_response()

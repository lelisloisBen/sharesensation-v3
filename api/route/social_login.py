from wsgiref import validate
import flask_restx
import tweepy
from api import api
from api.utils.social import (
    save_google_info_from_token,
    save_facebook_info_from_token,
    save_social_info_from_token,
    save_twitter_info_from_token,
    social_auth_redirect,
)
from database import db
from database.model.OAuth import OAuth
from flask import current_app as app
from flask import flash, redirect, render_template, request, session, url_for
from flask_dance.consumer import oauth_authorized, oauth_error
from flask_dance.consumer.storage.sqla import SQLAlchemyStorage
from flask_dance.contrib.facebook import facebook, make_facebook_blueprint
from flask_dance.contrib.google import google, make_google_blueprint
from flask_restx import Resource
from sqlalchemy.orm.exc import NoResultFound

google_blueprint = make_google_blueprint(
    client_id=app.config["OAUTH_CREDENTIALS"]["google"]["id"],
    client_secret=app.config["OAUTH_CREDENTIALS"]["google"]["secret"],
    scope=[
        "openid",
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/userinfo.profile",
    ],
)

facebook_blueprint = make_facebook_blueprint(
    client_id=app.config["OAUTH_CREDENTIALS"]["facebook"]["id"],
    client_secret=app.config["OAUTH_CREDENTIALS"]["facebook"]["secret"],
    scope=["email"],
)

google_bp = make_google_blueprint(storage=SQLAlchemyStorage(OAuth, db.session))

facebook_bp = make_facebook_blueprint(storage=SQLAlchemyStorage(OAuth, db.session))

social_ns = api.namespace("social", validate=True)


@social_ns.route("/")
class SocialAuthAPI(Resource):
    def get(self, *args, **kwargs):
        """User Signup"""
        login = request.args.get("login", None)
        signup = request.args.get("signup", None)
        session["is_signup"] = signup is not None
        social = login or signup
        if social == "twitter":
            return redirect(url_for("twitter"))
        elif social not in ["google", "facebook"]:
            return "Invalid url", 404
        else:
            return redirect(url_for(f"{social}.login"))


social_auth_model = social_ns.model(
    "Social Auth",
    {
        "social_name": flask_restx.fields.String(required=True),
        "access_token": flask_restx.fields.String(required=True),
        "access_token_secret": flask_restx.fields.String(required=False),
    },
    strict=True,
)


@social_ns.route("/signup")
class SocialSignupAPI(Resource):
    @social_ns.doc(body=social_auth_model, validate=True)
    def post(self, *args, **kwargs):
        """
        Register user with social access token.
        If success, return user info and token to access this site.

        **Args**

        social_name can be google, facebook or twitter.
        For google and facebook, access_token must be provided
        For twitter, access_token and access_token_secret must be provided.
        """
        data = request.json
        return save_social_info_from_token(
            True,
            data.get("social_name", None),
            data.get("access_token", None),
            data.get("access_token_secret"),
        )


@social_ns.route("/login")
class SocialLoginAPI(Resource):
    @social_ns.doc(body=social_auth_model)
    def post(self, *args, **kwargs):
        """
        Login user with social access token.
        If success, return user info and token to access this site.

        **Args**

        social_name can be google, facebook or twitter.
        For google and facebook, access_token must be provided
        For twitter, access_token and access_token_secret must be provided.
        """
        data = request.json
        return save_social_info_from_token(
            False,
            data.get("social_name", None),
            data.get("access_token", None),
            data.get("access_token_secret"),
        )


@app.route("/api/login/twitter", methods=["GET"])
def twitter(*args, **kwargs):
    auth = tweepy.OAuthHandler(
        app.config["OAUTH_CREDENTIALS"]["twitter"]["id"],
        app.config["OAUTH_CREDENTIALS"]["twitter"]["secret"],
        callback=app.config["BACKEND_URL"] + url_for("twitter_callback"),
    )
    return redirect(auth.get_authorization_url())


@app.route("/login/twitter/authorized", methods=["GET", "POST"])
def twitter_callback(*args, **kwargs):
    args = request.args
    oauth_token = args["oauth_token"]
    oauth_verifier = args["oauth_verifier"]
    auth = tweepy.OAuthHandler(
        app.config["OAUTH_CREDENTIALS"]["twitter"]["id"],
        app.config["OAUTH_CREDENTIALS"]["twitter"]["secret"],
    )
    auth.request_token = {
        "oauth_token": oauth_token,
        "oauth_token_secret": oauth_verifier,
    }
    token, secret = auth.get_access_token(oauth_verifier)

    is_signup = session.get("is_signup", False)
    user, code = save_twitter_info_from_token(is_signup, token, secret)
    return social_auth_redirect(user, code)


@oauth_authorized.connect_via(google_blueprint)
def google_logged_in(blueprint, token):
    is_signup = session.get("is_signup", False)
    user, code = save_google_info_from_token(is_signup, token["access_token"])
    return social_auth_redirect(user, code)


@oauth_error.connect_via(google_blueprint)
def google_error(blueprint, message, response):
    msg = ("OAuth error from {name}! " "message={message} response={response}").format(
        name=blueprint.name, message=message, response=response
    )
    flash(msg, category="error")


@oauth_authorized.connect_via(facebook_blueprint)
def facebook_logged_in(blueprint, token):
    is_signup = session.get("is_signup", False)
    user, code = save_facebook_info_from_token(is_signup, token["access_token"])
    return social_auth_redirect(user, code)


@oauth_error.connect_via(facebook_blueprint)
def facebook_error(blueprint, message, response):
    msg = ("OAuth error from {name}! " "message={message} response={response}").format(
        name=blueprint.name, message=message, response=response
    )
    flash(msg, category="error")

import flask_restx
import tweepy
from api import api
from api.utils.social import (
    get_facebook_info_from_token,
    get_google_info_from_token,
    save_social_and_redirect,
    save_social_info,
    get_twitter_info_from_token,
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


signup_model = social_ns.model(
    "Social Signup",
    {
        "access_token": flask_restx.fields.String(required=True),
        "social": flask_restx.fields.String(required=True),
    },
)


@social_ns.route("/signup")
class SocialSignupAPI(Resource):
    @social_ns.doc(body=signup_model)
    def post(self, *args, **kwargs):
        import requests

        data = request.json
        token = data["access_token"]
        res = requests.get(
            f"https://www.googleapis.com/oauth2/v2/userinfo?access_token={token}"
        )
        return "", 200


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

    info = get_twitter_info_from_token(token, secret)
    is_signup = session.get("is_signup", False)
    return save_social_and_redirect(
        is_signup, "twitter", token, info.id, info.screen_name, None
    )


@oauth_authorized.connect_via(google_blueprint)
def google_logged_in(blueprint, token):
    info = get_google_info_from_token(token["access_token"])
    if not info:
        app.logger(f"Invalid google token: {token}")
        return

    is_signup = session.get("is_signup", False)
    return save_social_and_redirect(
        is_signup, "google", token, info["id"], info["name"], info["email"]
    )


@oauth_error.connect_via(google_blueprint)
def google_error(blueprint, message, response):
    msg = ("OAuth error from {name}! " "message={message} response={response}").format(
        name=blueprint.name, message=message, response=response
    )
    flash(msg, category="error")


@oauth_authorized.connect_via(facebook_blueprint)
def facebook_logged_in(blueprint, token):
    info = get_facebook_info_from_token(token["access_token"])
    if not info:
        app.logger(f"Invalid facebook token: {token}")
        return

    is_signup = session.get("is_signup", False)
    return save_social_and_redirect(
        is_signup, "facebook", token, info["id"], info["name"], info["email"]
    )


@oauth_error.connect_via(facebook_blueprint)
def facebook_error(blueprint, message, response):
    msg = ("OAuth error from {name}! " "message={message} response={response}").format(
        name=blueprint.name, message=message, response=response
    )
    flash(msg, category="error")

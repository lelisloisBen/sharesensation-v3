from posixpath import split
from flask import Flask, render_template, redirect, url_for, flash, Blueprint, session
from flask_dance.contrib.github import make_github_blueprint, github
from flask_dance.contrib.google import make_google_blueprint, google
from flask_dance.contrib.facebook import make_facebook_blueprint, facebook
from flask_dance.contrib.twitter import make_twitter_blueprint, twitter
from flask_dance.consumer import oauth_authorized, oauth_error
from flask_dance.consumer.storage.sqla import SQLAlchemyStorage
from sqlalchemy.orm.exc import NoResultFound
from database.model.User import User
from database.model.OAuth import OAuth
from flask_restx import Resource
from flask import current_app as app
from database import db
from api import api
from flask import request
from api.utils.other import split_name

google_blueprint = make_google_blueprint(client_id=app.config['OAUTH_CREDENTIALS']['google']['id'], client_secret=app.config['OAUTH_CREDENTIALS']['google']['secret'],  scope=[
        "openid",
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/userinfo.profile",
    ]
)

facebook_blueprint = make_facebook_blueprint(client_id=app.config['OAUTH_CREDENTIALS']['facebook']['id'], client_secret=app.config['OAUTH_CREDENTIALS']['facebook']['secret'], scope = [
    "email"
    ]
)

twitter_blueprint = make_twitter_blueprint(api_key=app.config['OAUTH_CREDENTIALS']['twitter']['id'], api_secret=app.config['OAUTH_CREDENTIALS']['twitter']['secret'])

google_bp = make_google_blueprint(storage = SQLAlchemyStorage(OAuth, db.session))

facebook_bp = make_facebook_blueprint(storage = SQLAlchemyStorage(OAuth, db.session))

twitter_bp = make_twitter_blueprint(storage = SQLAlchemyStorage(OAuth, db.session))

social_ns = api.namespace("social", validate=True)
@social_ns.route("/")
class SocialAuthAPI(Resource):
    def get(self, *args, **kwargs):
        """User Signup"""
        login = request.args.get('login', None)
        signup = request.args.get('signup', None)
        session['is_signup'] = signup is not None
        social = login or signup
        if social not in ["google", "facebook", "twitter"]:
            return 'Invalid url', 404
        return redirect(url_for(f"{social}.login"))


@oauth_authorized.connect_via(google_blueprint)
def google_logged_in(blueprint, token):
    if not token:
        flash("Failed to log in.", category="error")
        return 
    resp = blueprint.session.get("/oauth2/v2/userinfo")
    if not resp.ok:
        msg = "Failed to fetch user info."
        flash(msg, category="error")
        return

    google_info = resp.json()
    print(google_info)

    query = OAuth.query.filter_by(
        provider = blueprint.name, provider_user_id = google_info["id"]
    )    
    try:
        oauth = query.one()
    except NoResultFound:
        google_user_login = google_info["name"]

        oauth = OAuth(
            provider=blueprint.name,
            provider_user_id=google_info["id"],
            provider_user_login=google_user_login,
            token=token,
        )

    # if session.get('is_signup', False):
    #     error = False
    #     if not oauth.user:
    #         try:
    #             user = User(
    #                 email = google_info["email"],
    #                 firstname = google_info["given_name"],
    #                 lastname = google_info["family_name"],
    #                 # avatar = google_info["picture"],
    #             )

    #             oauth.user = user
    #             db.session.add_all([user, oauth])
    #             db.session.commit()
    #         except:
    #             error = True
    #     else:
    #         error = True
    #     if error:
    #         return redirect(app.config['FRONTEND_URL'] + '/register?error=409')
    # else:
    #     user = oauth.user
    #     if not user:
    #         # del google_blueprint.token
    #         return redirect(app.config['FRONTEND_URL'] + '/login?error=401')
    
    # token = user.get_auth_token()
    # return redirect(app.config['FRONTEND_URL'] + '/?token=' + token)
    return redirect(app.config['FRONTEND_URL'])

@oauth_error.connect_via(google_blueprint)
def google_error(blueprint, message, response):
    msg = ("OAuth error from {name}! " "message={message} response={response}").format(
        name=blueprint.name, message = message, response = response
    )    
    flash(msg, category = "error")

@oauth_authorized.connect_via(facebook_blueprint)
def facebook_logged_in(blueprint,token):                  
    if not token:
        flash("Failed to log in.", category="error")
        return 

    resp = blueprint.session.get("/me")
    if not resp.ok:
        msg = "Failed to fetch user info."
        flash(msg, category="error")
        return 

    facebook_name = resp.json()["name"]
    facebook_user_id = resp.json()["id"]

    query = OAuth.query.filter_by(
        provider = blueprint.name, 
        provider_user_id = facebook_user_id
    )
    try:
        oauth = query.one()
    except NoResultFound:
        oauth = OAuth(
            provider = blueprint.name, 
            provider_user_id = facebook_user_id, 
            token = token
        )

    if session.get('is_signup', False):
        error = False
        if not oauth.user:
            try:
                first_name, last_name = split_name(facebook_name)
                user = User(
                    email = resp.json()["email"],
                    firstname = first_name,
                    lastname = last_name,
                    # avatar = google_info["picture"],
                )

                oauth.user = user
                db.session.add_all([user, oauth])
                db.session.commit()
            except:
                error = True
        else:
            error = True
        if error:
            return redirect(app.config['FRONTEND_URL'] + '/register?error=409')
    else:
        user = oauth.user
        if not user:
            return redirect(app.config['FRONTEND_URL'] + '/login?error=401')
    
    token = user.get_auth_token()
    return redirect(app.config['FRONTEND_URL'] + '/?token=' + token)            

@oauth_error.connect_via(facebook_blueprint)
def facebook_error(blueprint, message, response):
    msg = ("OAuth error from {name}! " "message={message} response={response}").format(
        name=blueprint.name, message=message, response=response
    )
    flash(msg, category="error")

@oauth_authorized.connect_via(twitter_blueprint)
def twitter_logged_in(blueprint,token):                  
    if not token:
        flash("Failed to log in.", category="error")
        return 

    resp = blueprint.session.get('account/verify_credentials.json')
    if not resp.ok:
        msg = "Failed to fetch user info."
        flash(msg, category="error")
        return 

    twitter_name = resp.json()["screen_name"]
    twitter_user_id = resp.json()["id"]

    query = OAuth.query.filter_by(
        provider = blueprint.name, 
        provider_user_id = twitter_user_id
    )
    try:
        oauth = query.one()
    except NoResultFound:
        oauth = OAuth(
            provider = blueprint.name, 
            provider_user_id = twitter_user_id, 
            token = token
        )

    if session.get('is_signup', False):
        error = False
        if not oauth.user:
            try:
                first_name, last_name = split_name(twitter_name)
                user = User(
                    email = resp.json()["email"],
                    firstname = first_name,
                    lastname = last_name,
                )

                oauth.user = user
                db.session.add_all([user, oauth])
                db.session.commit()
            except:
                error = True
        else:
            error = True
        if error:
            return redirect(app.config['FRONTEND_URL'] + '/register?error=409')
    else:
        user = oauth.user
        if not user:
            return redirect(app.config['FRONTEND_URL'] + '/login?error=401')
    
    token = user.get_auth_token()
    return redirect(app.config['FRONTEND_URL'] + '/?token=' + token)

@oauth_error.connect_via(twitter_blueprint)
def twitter_error(blueprint, message, response):
    msg = ("OAuth error from {name}! " "message={message} response={response}").format(
        name=blueprint.name, message=message, response=response
    )
    flash(msg, category="error")
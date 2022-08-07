from datetime import datetime
from logging.config import valid_ident
from posixpath import split
from re import L
from unicodedata import name
from wsgiref import validate
from flask import Flask, render_template, redirect, url_for, flash, Blueprint, session
from flask_dance.contrib.github import make_github_blueprint, github
from flask_dance.contrib.google import make_google_blueprint, google
from flask_dance.contrib.facebook import make_facebook_blueprint, facebook
# from api.utils.twitter import make_twitter_blueprint, twitter
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
import tweepy
from flask import url_for

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

# twitter_blueprint = make_twitter_blueprint(api_key=app.config['OAUTH_CREDENTIALS']['twitter']['id'], api_secret=app.config['OAUTH_CREDENTIALS']['twitter']['secret'])

google_bp = make_google_blueprint(storage = SQLAlchemyStorage(OAuth, db.session))

facebook_bp = make_facebook_blueprint(storage = SQLAlchemyStorage(OAuth, db.session))

# twitter_bp = make_twitter_blueprint(storage = SQLAlchemyStorage(OAuth, db.session))



social_ns = api.namespace("social", validate=True)
@social_ns.route("/")
class SocialAuthAPI(Resource):
    def get(self, *args, **kwargs):
        """User Signup"""
        login = request.args.get('login', None)
        signup = request.args.get('signup', None)
        session['is_signup'] = signup is not None
        social = login or signup
        if social == 'twitter':
            return redirect(url_for('twitter'))
        elif social not in ["google", "facebook"]:
            return 'Invalid url', 404
        else:
            return redirect(url_for(f"{social}.login"))


@app.route("/api/login/twitter", methods=['GET'])
def twitter(*args, **kwargs):
    print(app.config['BACKEND_URL'] + url_for('twitter_callback'))
    auth = tweepy.OAuthHandler(app.config['OAUTH_CREDENTIALS']['twitter']['id'], app.config['OAUTH_CREDENTIALS']['twitter']['secret'], 
        callback=app.config['BACKEND_URL'] + url_for('twitter_callback'))
    return redirect(auth.get_authorization_url())


@app.route("/login/twitter/authorized", methods=['GET', 'POST'])
def twitter_callback(*args, **kwargs):
    args = request.args
    oauth_token = args['oauth_token']
    oauth_verifier = args['oauth_verifier']
    auth = tweepy.OAuthHandler(app.config['OAUTH_CREDENTIALS']['twitter']['id'], app.config['OAUTH_CREDENTIALS']['twitter']['secret'])
    auth.request_token = {'oauth_token': oauth_token, 'oauth_token_secret': oauth_verifier}
    auth.get_access_token(oauth_verifier)

    api = tweepy.API(auth)
    res = api.verify_credentials(include_email='true')

    query = OAuth.query.filter_by(
        provider = "twitter", provider_user_id = str(res.id)
    )   
    try:
        oauth = query.one()
    except NoResultFound:
        twitter_user_login = res.screen_name

        oauth = OAuth(
            provider="twitter",
            provider_user_id=str(res.id),
            provider_user_login=twitter_user_login,
            # token=token,
        )

    if session.get('is_signup', False):
        error = False
        if not oauth.user:
            try:
                first_name, last_name = split_name(res.screen_name)
                user = User(
                    email = res.email,
                    firstname = first_name,
                    lastname = last_name,
                    confirmed=True,
                    confirmed_on=datetime.now(),
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

    print(google_info["id"])
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
            # token=token,
        )

    if session.get('is_signup', False):
        error = False
        if not oauth.user:
            try:
                first_name, last_name = split_name(google_info['name'])
                user = User(
                    email = google_info["email"],
                    firstname = first_name,
                    lastname = last_name,
                    confirmed=True,
                    confirmed_on=datetime.now(),
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
            # del google_blueprint.token
            return redirect(app.config['FRONTEND_URL'] + '/login?error=401')
    
    token = user.get_auth_token()
    return redirect(app.config['FRONTEND_URL'] + '/?token=' + token)

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

    resp = blueprint.session.get("/me?fields=id,name,email")
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
                    confirmed=True,
                    confirmed_on=datetime.now(),
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

# @oauth_authorized.connect_via(twitter_blueprint)
# def twitter_logged_in(blueprint,token):
#     if not token:
#         flash("Failed to log in.", category="error")
#         return False

#     resp = blueprint.session.get("account/verify_credentials.json")
#     if not resp.ok:
#         msg = "Failed to fetch user info."
#         flash(msg, category="error")
#         return False

#     info = resp.json()
#     user_id = info["id_str"]

#     # Find this OAuth token in the database, or create it
#     query = OAuth.query.filter_by(
#         provider=blueprint.name,
#         provider_user_id=user_id,
#     )
#     try:
#         oauth = query.one()
#     except NoResultFound:
#         oauth = OAuth(
#             provider=blueprint.name,
#             provider_user_id=user_id,
#             token=token,
#         )

#     if session.get('is_signup', False):
#         error = False
#         if not oauth.user:
#             try:
#                 first_name, last_name = split_name(info["screen_name"])
#                 user = User(
#                     email = info["email"],
#                     firstname = first_name,
#                     lastname = last_name,
#                     confirmed=True,
#                     confirmed_on=datetime.now(),
#                 )

#                 oauth.user = user
#                 db.session.add_all([user, oauth])
#                 db.session.commit()
#             except:
#                 error = True
#         else:
#             error = True
#         if error:
#             return redirect(app.config['FRONTEND_URL'] + '/register?error=409')
#     else:
#         user = oauth.user
#         if not user:
#             return redirect(app.config['FRONTEND_URL'] + '/login?error=401')
    
#     token = user.get_auth_token()
#     return redirect(app.config['FRONTEND_URL'] + '/?token=' + token)

# @oauth_error.connect_via(twitter_blueprint)
# def twitter_error(blueprint, message, response):
#     msg = ("OAuth error from {name}! " "message={message} response={response}").format(
#         name=blueprint.name, message=message, response=response
#     )
#     flash(msg, category="error")
from datetime import datetime

import flask
import requests
import tweepy
import tweepy.errors
from api.schema.User import UserSchema
from api.utils.other import split_name
from database import db
from database.model.OAuth import OAuth
from database.model.User import User
from flask import current_app as app
from flask import redirect
from sqlalchemy.orm.exc import NoResultFound


def save_social_info(is_signup, social_name, token, social_id, name, email=None):
    query = OAuth.query.filter_by(provider=social_name, provider_user_id=str(social_id))
    try:
        oauth = query.one()
    except NoResultFound:
        user_login = name
        print(token, type(token))

        oauth = OAuth(
            provider=social_name,
            provider_user_id=str(social_id),
            provider_user_login=user_login,
            token=token,
        )

    if is_signup:
        error = False
        if not oauth.user:
            try:
                first_name, last_name = split_name(name)
                user = User(
                    email=email,
                    firstname=first_name,
                    lastname=last_name,
                    confirmed=True,
                    confirmed_on=datetime.now(),
                    # avatar = google_info["picture"],
                )

                oauth.user = user
                db.session.add_all([user, oauth])
                db.session.commit()
            except Exception as e:
                app.logger.critical(str(e))
                error = True
        else:
            error = True
        if error:
            return "", 409
    else:
        user = oauth.user
        if not user:
            return "", 401

    return user, 200


def social_auth_redirect(data, code):
    if code == 401:
        return redirect(app.config["FRONTEND_URL"] + "/login?error=401")
    elif code == 409:
        return redirect(app.config["FRONTEND_URL"] + "/register?error=409")
    elif code != 200:
        app.logger.critical(f"Error: {code}\nMessage: {data}")
        return redirect(app.config["FRONTEND_URL"] + "/login?error=401")
    else:
        user = data
        return redirect(app.config["FRONTEND_URL"] + "/?token=" + user.get_auth_token())


def save_google_info_from_token(is_signup, token):
    if not token:
        return "Invalid token", 400
    res = requests.get(
        f"https://www.googleapis.com/oauth2/v2/userinfo?access_token={token}"
    )
    if not res.ok:
        return "Invalid token", 400

    data = res.json()
    return save_social_info(
        is_signup,
        "google",
        {"access_token": token},
        data["id"],
        data["name"],
        data["email"],
    )


def save_facebook_info_from_token(is_signup, token):
    if not token:
        return "Invalid token", 400
    res = requests.get(
        f"https://graph.facebook.com/me?fields=id,name,email&access_token={token}"
    )
    if not res.ok:
        return "Invalid token", 400

    data = res.json()
    return save_social_info(
        is_signup,
        "facebook",
        {"access_token": token},
        data["id"],
        data["name"],
        data["email"],
    )


def save_twitter_info_from_token(is_signup, token, token_secret):
    if not token or not token_secret:
        return "Invalid token", 400
    auth = tweepy.OAuthHandler(
        app.config["OAUTH_CREDENTIALS"]["twitter"]["id"],
        app.config["OAUTH_CREDENTIALS"]["twitter"]["secret"],
    )
    auth.access_token = token
    auth.access_token_secret = token_secret
    api = tweepy.API(auth)
    try:
        user = api.verify_credentials(include_email="true")
    except tweepy.errors.Unauthorized:
        return "Invalid token", 400

    return save_social_info(
        is_signup,
        "twitter",
        {
            "access_token": token,
            "access_token_secret": token_secret,
        },
        user.id,
        user.name,
        None,
    )


def save_social_info_from_token(is_signup, social_name, token, token_secret):
    if social_name == "google":
        user, code = save_google_info_from_token(is_signup, token)
    elif social_name == "facebook":
        user, code = save_facebook_info_from_token(is_signup, token)
    elif social_name == "twitter":
        user, code = save_twitter_info_from_token(is_signup, token, token_secret)
    else:
        return "Invalid social name", 400
    if code == 200:
        resp = UserSchema().dump(user)
        resp["token"] = user.get_auth_token()
        return flask.jsonify(resp)
    else:
        return user, code
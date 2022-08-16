from datetime import datetime

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

    return user.get_auth_token(), ""


def save_social_and_redirect(
    is_signup, social_name, token, social_id, name, email=None
):
    data, error = save_social_info(
        is_signup, social_name, token, social_id, name, email=None
    )
    if error == 401:
        return redirect(app.config["FRONTEND_URL"] + "/login?error=401")
    elif error == 409:
        return redirect(app.config["FRONTEND_URL"] + "/register?error=409")
    elif error:
        app.logger.critical(f"Error: {error}\nMessage: {data}")
        return redirect(app.config["FRONTEND_URL"] + "/register?error=401")
    else:
        token = data.get_auth_token()
        return redirect(app.config["FRONTEND_URL"] + "/?token=" + data)
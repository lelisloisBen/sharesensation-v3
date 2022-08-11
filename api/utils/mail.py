import re
from flask import render_template
from flask_mail import Message
from api import mail
import requests
from flask import current_app as app

def valid_email_format(email):
    return bool(re.search(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", email))

def send_verify_email(user):
    token = user.get_verify_token()

    subject = "ShareSensation: Verify email"
    html = render_template('email/verify_email.html', frontend_url = app.config["FRONTEND_URL"], user = user, token = token)

    # msg = Message()
    # msg.subject = subject
    # # msg.sender = 'username@gmail.com'
    # msg.recipients = [user.email]
    # msg.html = html

    # mail.send(msg)

    send_by_mailgun([user.email], subject, html)

def send_by_mailgun(recipient, subject, text):
    # print(app.config['MAILGUN_DOMAIN'])
    res = requests.post(
        f"https://api.mailgun.net/v3/{app.config['MAILGUN_DOMAIN']}/messages",
        auth=("api", app.config["MAILGUN_API_KEY"]),
        # data={"from": f"<postmaster@{app.config['MAILGUN_DOMAIN']}>",
        data={"from": "Samirbenzada@gmail.com",
              "to": recipient,
              "subject": subject,
              "html": text})
    # print(res, res.json())

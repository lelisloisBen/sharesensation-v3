import re
from utils import render_template
from flask_mail import Message
from api import mail

def valid_email_format(email):
    return bool(re.search(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", email))

def send_verify_email(user):
    token = user.get_verify_token()

    msg = Message()
    msg.subject = "Login System: Verify email"
    msg.sender = 'username@gmail.com'
    msg.recipients = [user.email]
    msg.html = render_template('email/verify_email.html', user = user, token = token)

    mail.send(msg)
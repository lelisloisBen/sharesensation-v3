from time import time

import jwt
from database import db
from flask import current_app as app


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    firstname = db.Column(db.String(120), nullable=False)
    lastname = db.Column(db.String(120))
    password = db.Column(db.String(80), nullable=False)
    avatar = db.Column(db.String(220), default="avatar.png")
    wallet = db.Column(db.Float(5), default=0)
    birthdate = db.Column(db.String(120))
    gender = db.Column(db.String(120))
    address = db.Column(db.String(120))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    zipCode = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    admin = db.Column(db.Integer)

    def __repr__(self):
        return "<User %r>" % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "avatar": self.avatar,
            "wallet": self.wallet,
            "birthdate": self.birthdate,
            "gender": self.gender,
            "address": self.address,
            "city": self.city,
            "state": self.state,
            "zipCode": self.zipCode,
            "phone": self.phone,
            "admin": self.admin,
        }

    def get_verify_token(self, expires=500):
        return jwt.encode(
            {"verify_email": self.email, "exp": time() + expires},
            app.config["SECRET_KEY"],
            algorithm="HS256",
        )

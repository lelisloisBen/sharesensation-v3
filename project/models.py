import os
from . import db
from flask import current_app as app
from flask_login import UserMixin
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin
import jwt
from time import time

class User(UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(120), unique=True, nullable=False)
  username = db.Column(db.String(120), nullable=False)
  password = db.Column(db.String(120), nullable=False)
  avatar = db.Column(db.String(220), default='avatar.png')
  wallet = db.Column(db.Float(5), default=0)
  birthdate = db.Column(db.String(120))
  gender = db.Column(db.String(120))
  address = db.Column(db.String(120))
  city = db.Column(db.String(120))
  state = db.Column(db.String(120))
  zipCode = db.Column(db.String(120))
  phone = db.Column(db.String(120))
  admin = db.Column(db.Integer)
  is_active = db.Column(db.Boolean, default=True)
  confirmed = db.Column(db.Boolean, nullable=False, default=False)
  confirmed_on = db.Column(db.DateTime, nullable=True)

  def __repr__(self):
      return 'User {}'.format(self.email)

  def get_reset_token(self, expires=500):
    return jwt.encode(
      {'reset_password': self.email, 'exp': time() + expires},
      app.config['SECRET_KEY'], algorithm='HS256')
  
  def get_verify_token(self, expires=500):
    return jwt.encode(
      {'verify_email': self.email, 'exp': time() + expires},
      app.config['SECRET_KEY'], algorithm='HS256')

  @staticmethod
  def verify_reset_token(token):
    try:
      email = jwt.decode(token, app.config['SECRET_KEY'], 
                              algorithms='HS256')['reset_password']
    except:
      return
    return User.query.filter_by(email = email).first()    

  @staticmethod
  def verify_email_token(token):
    try:
      email = jwt.decode(token, app.config['SECRET_KEY'], 
                              algorithms='HS256')['verify_email']
    except:
      return
    return User.query.filter_by(email = email).first()    

  @staticmethod
  def verify_email(email):
    user = User.query.filter_by(email = email).first()
    return user

  def get_id(self):
    return self.id

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
      "admin": self.admin
    }


class OAuth(OAuthConsumerMixin, db.Model):
  __table_args__ = (db.UniqueConstraint("provider", "provider_user_id"),)
  provider_user_id = db.Column(db.String(256), nullable = False)
  provider_user_login = db.Column(db.String(256))
  user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable = False)
  user = db.relationship(User)

class Activities(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  cat =  db.Column(db.String(120))
  name = db.Column(db.String(120))
  path = db.Column(db.String(120))

  def __repr__(self):
    return '<activities %r>' % self.cat

  def serialize(self):
    return {
      "id": self.id,
      "cat": self.cat,
      "name": self.name,
      "path": self.path
    }


class Saletaxes(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  country =  db.Column(db.String(100))
  state = db.Column(db.String(100))
  letters = db.Column(db.String(100))
  rate = db.Column(db.String(220))

  def __repr__(self):
    return '<saletaxes %r>' % self.country

  def serialize(self):
    return {
      "id": self.id,
      "country": self.country,
      "state": self.state,
      "letters": self.letters,
      "rate": self.rate
    }

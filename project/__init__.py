from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from flask_mail import Mail
import os 

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

db = SQLAlchemy()
jwt = JWTManager()
mail = Mail()

def create_app():
  app = Flask(__name__)

  app.config['SECRET_KEY'] = 'key-goes-here'
  app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('JAWSDB_URL')
  # app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
  # app.config['MAIL_PORT'] = 587
  app.config['MAIL_SERVER'] = '127.0.0.1'
  app.config['MAIL_PORT'] = 1025
  app.config['GOOGLE_CLIENT_ID'] = os.environ.get('GOOGLE_CLIENT_ID')
  app.config['GOOGLE_CLIENT_SECRET'] = os.environ.get('GOOGLE_CLIENT_SECRET')
  app.config['FACEBOOK_CLIENT_ID'] = os.environ.get('FACEBOOK_CLIENT_ID')
  app.config['FACEBOOK_CLIENT_SECRET'] = os.environ.get('FACEBOOK_CLIENT_SECRET')
  app.config['TWIITER_API_KEY'] = os.environ.get('TWIITER_API_KEY')
  app.config['TWITTER_API_SECRET'] = os.environ.get('TWITTER_API_SECRET')
  # app.config['MAIL_USE_TLS'] = True

  db.init_app(app)

  login_manager = LoginManager()
  login_manager.login_view = 'auth.login'
  login_manager.init_app(app)

  jwt.init_app(app)
  mail.init_app(app)

  from .models import User, OAuth

  # @login_manager.user_loader
  # def load_user(user_id):
  #   return User.query.get(int(user_id))

  #blueprints auth routes
  from .auth import auth as auth_blueprint
  app.register_blueprint(auth_blueprint)

  # from .social_login import github_blueprint
  # app.register_blueprint(github_blueprint, url_prefix = "/login")

  from .social_login import google_blueprint
  app.register_blueprint(google_blueprint, url_prefix = "/login")

  from .social_login import facebook_blueprint
  app.register_blueprint(facebook_blueprint, url_prefix = "/login")

  from .social_login import twitter_blueprint
  app.register_blueprint(twitter_blueprint, url_prefix = "/login")

  #non-auth parts
  from .main import main as main_blueprint
  app.register_blueprint(main_blueprint)

  return app
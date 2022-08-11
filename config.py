import os

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = '57e19ea558d4967a552d03deece34a70'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('JAWSDB_URL')
    
    # Social Auth
    OAUTH_CREDENTIALS = {
        'google': {
            'id': os.environ.get('GOOGLE_CLIENT_ID'),
            'secret': os.environ.get('GOOGLE_CLIENT_SECRET'),
        },
        'facebook': {
            'id' : os.environ.get('FACEBOOK_CLIENT_ID'),
            'secret': os.environ.get('FACEBOOK_CLIENT_SECRET'),
        },
        'twitter': {
            'id': os.environ.get('TWITTER_API_ID'),
            'secret': os.environ.get('TWITTER_API_SECRET'),
        }
    }

class ProductionConfig(Config):
    DEBUG = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = os.environ.get('MAIL_PORT')
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    FRONTEND_URL = 'https://sharesensation.herokuapp.com'

class DevelopmentConfig(Config):
    ENV="development"
    DEVELOPMENT=True
    DEBUG=True
    MAIL_SERVER = '127.0.0.1'
    MAIL_PORT = 1025
    FRONTEND_URL = 'http://localhost:3000'
    
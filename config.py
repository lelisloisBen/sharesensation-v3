import os

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = '57e19ea558d4967a552d03deece34a70'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('JAWSDB_URL')
    
    # Social Auth
    GOOGLE_CLIENT_ID = '12207959911-8uha1ng75g9ic846a1r58lk6va4rdatg.apps.googleusercontent.com'
    GOOGLE_CLIENT_SECRET = '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'
    FACEBOOK_CLIENT_ID = ''
    FACEBOOK_CLIENT_SECRET = ''
    TWIITER_API_KEY = ''
    TWITTER_API_SECRET = ''

class ProductionConfig(Config):
    DEBUG = False
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587

class DevelopmentConfig(Config):
    ENV="development"
    DEVELOPMENT=True
    DEBUG=True
    MAIL_SERVER = '127.0.0.1'
    MAIL_PORT = 1025
    
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
            'id': '12207959911-8uha1ng75g9ic846a1r58lk6va4rdatg.apps.googleusercontent.com',
            'secret': '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',
        },
        'facebook': {
            'id' : '',
            'secret': '',
        },
        'twitter': {
            'id': '',
            'secret': '',
        }
    }

class ProductionConfig(Config):
    DEBUG = False
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    FRONTEND_URL = 'https://sharesensation.herokuapp.com'

class DevelopmentConfig(Config):
    ENV="development"
    DEVELOPMENT=True
    DEBUG=True
    MAIL_SERVER = '127.0.0.1'
    MAIL_PORT = 1025
    FRONTEND_URL = 'http://localhost:3000'
    
from flask import Flask, Blueprint
import database
from flask_cors import CORS
from api import api, mail
from api.route.auth import auth_ns

def create_app():
    app = Flask(__name__)
    # setup with the configuration provided
    app.config.from_object('config.DevelopmentConfig')

    CORS(app)
    
    # setup all our dependencies
    database.init_app(app)
    mail.init_app(app)
    
    # register blueprint
    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)
    app.register_blueprint(blueprint)
    
    return app

if __name__ == "__main__":
    create_app().run()
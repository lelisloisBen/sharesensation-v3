from flask import Flask, Blueprint
import database

from api import api, mail
from api.route.auth import auth_ns

def create_app():
    app = Flask(__name__)
    # setup with the configuration provided
    app.config.from_object('config.DevelopmentConfig')
    
    # setup all our dependencies
    database.init_app(app)
    
    # register blueprint
    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)
    app.register_blueprint(blueprint)
    
    return app

if __name__ == "__main__":
    create_app().run()
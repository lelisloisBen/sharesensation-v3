from flask import Flask, Blueprint
import database
from flask_cors import CORS
from api import api, mail
from api.route.auth import auth_ns

def create_app():
    app = Flask(__name__)
    # setup with the configuration provided
    app.config.from_object('config.ProductionConfig')
    # app.config.from_object('config.DevelopmentConfig')

    CORS(app)
    
    # setup all our dependencies
    database.init_app(app)
    mail.init_app(app)

    with app.app_context():
        from api.route.social_login import social_ns
        from api.route.social_login import google_blueprint, facebook_blueprint
        import api.route.other as router_other

        # register blueprint
        blueprint = Blueprint('api', __name__, url_prefix='/api')
        api.init_app(blueprint)
        app.register_blueprint(blueprint)

        # register social blueprints
        app.register_blueprint(google_blueprint, url_prefix = "/login")
        app.register_blueprint(facebook_blueprint, url_prefix = "/login")
        # app.register_blueprint(twitter_blueprint, url_prefix = "/login")
    
    return app

app = create_app()

@app.route('/')
def hello_world():
    return "<div style='text-align: center; background-color: orange'><h1>Backend running...</h1><br/><h3>Welcome back samir</h3><img src='https://media.gettyimages.com/photos/woman-sitting-by-washing-machine-picture-id117852649?s=2048x2048' width='80%' /></div>"

from flask_restx import Api
from flask_mail import Mail

# authorizations = {"Bearer Auth": {"type": "apiKey", "in": "header",
#                                     "name": "Authorization"}}
api = Api(
    title='Sharesensation API',
    doc='/doc',
    version="1.0",
    description="Welcome to the Swagger UI documentation site!",
    security='Session Auth',
    # authorizations=authorizations
)

mail = Mail()
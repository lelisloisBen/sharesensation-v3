from flask_restx import Api

authorizations = {"Bearer Auth": {"type": "apiKey", "in": "header",
                                    "name": "Authorization"}}
api = Api(
    title='Flask API with JWT-Based Authentication and for Publications Management',
    doc='/doc',
    version="1.0",
    description="Welcome to the Swagger UI documentation site!",
    security='Bearer Auth',
    authorizations=authorizations
)
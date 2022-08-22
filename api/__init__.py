from flask_restx import Api
from flask_mail import Mail

mail = Mail()

authorizations = {"Bearer Auth": {"type": "apiKey", "in": "header",
                                    "name": "Authorization"}}
api = Api(
    title='Sharesensation API',
    doc='/doc',
    version="1.0",
    description="""
# Authorization

You get token when you try to login.
Add it to header when you make a request.

```
{
    "Authorization": token,
}
```
""",
    security='Bearer Auth',
    authorizations=authorizations
)

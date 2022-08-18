from api import api
from flask_restx import Resource
from database.model.User import User
from database import db

user_ns = api.namespace("user", validate=True)


@user_ns.route("/email")
class DeleteUserByEmailAPI(Resource):
    def delete(self, *args, **kwargs):
        """
        Delete user having specified email
        
        m.ouberghouz@gmail.com and m.ouberghouz@hotmail.com
        """
        User.query.filter_by(email="m.ouberghouz@gmail.com").delete()
        User.query.filter_by(email="m.ouberghouz@hotmail.com").delete()
        db.session.commit()

        return ""
        
from api import api
from flask_restx import Resource
from database.model.User import User
from database.model.OAuth import OAuth
from database import db

user_ns = api.namespace("user", validate=True)


@user_ns.route("/email")
class DeleteUserByEmailAPI(Resource):
    def delete(self, *args, **kwargs):
        """
        Delete user having specified email
        
        m.ouberghouz@gmail.com and m.ouberghouz@hotmail.com
        """
        emails = ["m.ouberghouz@gmail.com", "m.ouberghouz@hotmail.com"]
        for email in emails:
            user = User.query.filter_by(email=email).first()
            if user:
                OAuth.query.filter_by(user_id=user.id).delete()
                db.session.delete(user)
        db.session.commit()

        return ""
        
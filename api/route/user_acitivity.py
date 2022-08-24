from distutils.command.upload import upload
from hashlib import sha224
from tokenize import String
from werkzeug.datastructures import FileStorage
from typing_extensions import Required
from wsgiref import validate
from api import api
from database.model.Category import Category
from flask_restx import Resource
from flask import jsonify, request
import flask_restx
from database.model.UserActivity import UserActivity
from database.model.UserActivityPrice import UserActivityPrice
from database.model.UserActivityTime import UserActivityTime
from database import db
from werkzeug.utils import secure_filename
from .auth import token_required
from flask import current_app as app
from api.utils.amazon import upload_file_to_s3
from database.model.UserActivity import UserActivity

user_activity_ns = api.namespace("user_activity", validate=True)

time_model = user_activity_ns.model(
    "Activity time",
    {
        "day": flask_restx.fields.Integer(required=True),
        "start_time": flask_restx.fields.String(required=True),
        "end_time": flask_restx.fields.String(required=True),
    },
    strict=True,
)

price_model = user_activity_ns.model(
    "Activity price",
    {
        "apply_index": flask_restx.fields.Integer(required=True),
        "total_price": flask_restx.fields.Float(required=True),
        "people_per_session": flask_restx.fields.Integer(required=True),
        "duration_session": flask_restx.fields.Integer(required=True),
        "detail": flask_restx.fields.String(required=True),
    },
    strict=True,
)

create_model = user_activity_ns.model(
    "Create user activity",
    {
        "activity_id": flask_restx.fields.Integer(required=True),
        "address": flask_restx.fields.String(required=True),
        "city": flask_restx.fields.String(required=True),
        "state": flask_restx.fields.String(required=True),
        "zipcode": flask_restx.fields.String(required=True),

        "title": flask_restx.fields.String(required=True),
        "description": flask_restx.fields.String(required=True),
        "note": flask_restx.fields.String(required=True),

        "cancelation": flask_restx.fields.String(required=True),
        "deposit": flask_restx.fields.Float(required=False),
        "reservation": flask_restx.fields.String(required=True),
        "requirement_info": flask_restx.fields.String(required=True),

        "languages": flask_restx.fields.List(flask_restx.fields.String(), required=True),
        "equipments": flask_restx.fields.List(flask_restx.fields.String(), required=True),
        "transportation": flask_restx.fields.Boolean(required=True),
        "transportation_from": flask_restx.fields.String(required=False),
        "transportation_to": flask_restx.fields.String(required=False),
        "min_age": flask_restx.fields.Integer(required=False),
        "max_age": flask_restx.fields.Integer(required=False),
        "min_height": flask_restx.fields.Integer(required=False),
        "max_height": flask_restx.fields.Integer(required=False),
        "min_weight": flask_restx.fields.Integer(required=False),
        "max_weight": flask_restx.fields.Integer(required=False),
        "procedure_rules": flask_restx.fields.String(required=False),
        
        "times": flask_restx.fields.List(flask_restx.fields.Nested(time_model, required=True)),
        "prices": flask_restx.fields.List(flask_restx.fields.Nested(price_model, required=True)),
    },
    strict=True,
)

upload_parser = user_activity_ns.parser()
upload_parser.add_argument("images[]", location="files", type=FileStorage, required=True, action="append")

@user_activity_ns.route("/")
class CreateUserActivityAPI(Resource):
    @user_activity_ns.doc(body=create_model, validate=True)
    @token_required
    def post(self, user, *args, **kwargs):
        """
        Create user activity.

        If it's successful, it returns created user activity id.

        Response:
            {
                "id": 1
            }
        """
        data = request.json
        times = data.pop("times")
        prices = data.pop("prices")
        new_activity = UserActivity(**data, user_id=user.id)
        db.session.add(new_activity)
        db.session.flush()
        for time in times:
            new_time = UserActivityTime(**time, user_activity_id=new_activity.id)
            db.session.add(new_time)
        for price in prices:
            new_price = UserActivityPrice(**price, user_activity_id=new_activity.id)
            db.session.add(new_price)
        db.session.commit()
        return {"id": new_activity.id}, 200

@user_activity_ns.route("/<int:user_activity_id>/images")
class UploadImagesAPI(Resource):
    @api.expect(upload_parser, validate=True)
    def post(self, user_activity_id):
        """
        Upload images for user activity

        Content-Type: multipart/form-data
        """
        user_activity = UserActivity.query.filter(UserActivity.id == user_activity_id).first_or_404()
        
        print(request.files)

        files = request.files.getlist("images")
        s3_path = []
        for file in files:
            file.filename = secure_filename(file.filename)
            path = upload_file_to_s3(file, app.config["S3_BUCKET"])
            s3_path.append(path)
        
        user_activity.images = s3_path
        db.session.commit()

        return ""
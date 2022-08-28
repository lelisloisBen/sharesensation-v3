from os import remove
from ssl import ALERT_DESCRIPTION_PROTOCOL_VERSION
import uuid
from io import BytesIO

import flask_restx
from api import api
from api.utils.amazon import resize_image_size, upload_file_to_s3
from api.utils.other import removeSpaces
from database import Activity, UserActivity, UserActivityPrice, UserActivityTime, db
from flask import current_app as app
from flask import jsonify, request
from flask_restx import Resource
from PIL import Image
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from api.schema.UserActivity import UserActivitySchema

from .auth import token_required

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
        "languages": flask_restx.fields.List(
            flask_restx.fields.String(), required=True
        ),
        "equipments": flask_restx.fields.List(
            flask_restx.fields.String(), required=True
        ),
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
        "company_name": flask_restx.fields.String(required=True),
        "company_state": flask_restx.fields.String(required=True),
        "company_ein": flask_restx.fields.String(required=True),
        "company_phone": flask_restx.fields.String(required=True),
        "company_website": flask_restx.fields.String(required=True),
        "times": flask_restx.fields.List(
            flask_restx.fields.Nested(time_model, required=True)
        ),
        "prices": flask_restx.fields.List(
            flask_restx.fields.Nested(price_model, required=True)
        ),
    },
    strict=True,
)

upload_parser = user_activity_ns.parser()
upload_parser.add_argument(
    "images[]", location="files", type=FileStorage, required=True, action="append"
)


@user_activity_ns.route("/")
class UserActivityAPI(Resource):
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

    @api.doc(params={"category": {"in": "query"}, "city": {"in": "query"}})
    def get(self, *args, **kwargs):
        """
        Get User Activity List

        Get all registered user activity list. You can filter by given fields.
        """
        query = UserActivity.query

        if category := request.args.get("category", None):
            query = query.join(Activity, Activity.id == UserActivity.activity_id).filter(Activity.cat == category)
        if city := request.args.get("city", None):
            query = query.filter(UserActivity.city == city)
        
        activities = query.all()

        return UserActivitySchema().dump(activities, many=True), 200

@user_activity_ns.route("/<int:user_activity_id>")
class UserActivitySingleAPI(Resource):
    def get(self, user_activity_id):
        user_activity = UserActivity.query.filter_by(id=user_activity_id).first_or_404()
        return UserActivitySchema().dump(user_activity), 200

@user_activity_ns.route("/<int:user_activity_id>/images")
class UploadImagesAPI(Resource):
    @api.expect(upload_parser, validate=True)
    def post(self, user_activity_id):
        """
        Upload images for user activity

        After create activity, you get user_activity_id.
        You can upload images for the activity by calling this API.

        Content-Type: multipart/form-data
        """
        user_activity = UserActivity.query.filter(
            UserActivity.id == user_activity_id
        ).first_or_404()

        files = request.files.getlist("images[]")
        s3_path = []
        for file in files:
            file_name = str(uuid.uuid4()) + "-" + secure_filename(file.filename)

            in_mem_file = BytesIO(file.read())
            image = Image.open(in_mem_file)
            image.thumbnail(resize_image_size(image.width, image.height))
            in_mem_file = BytesIO()
            image.save(in_mem_file, format="PNG")
            in_mem_file.seek(0)

            path = upload_file_to_s3(file, app.config["S3_BUCKET"], file_name)
            s3_path.append(path)

        user_activity.images = s3_path
        db.session.commit()

        return ""

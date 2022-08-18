from api import api
from database import Activity
from flask_restx import Resource, reqparse, inputs
from flask import jsonify
from api.schema.Activity import ActivitySchema
from flask import request
import flask_restx

activity_ns = api.namespace("activity", validate=True)

parser = reqparse.RequestParser()
parser.add_argument('category',
                    help="Filter by category",
                    required=False)

@activity_ns.route("/")
class ActivityListAPI(Resource):
    @activity_ns.expect(parser)
    def get(self, *args, **kwargs):
        """
        Get registered activity list

        You can filter activities by category name by query parameter
        ex: /activity?category=vip
        """
        category = request.args.get('category', None)
        if category:
            data = Activity.query.filter_by(cat=category).all()
        else:
            data = Activity.query.all()

        if not data:
            return jsonify({'msg':'Activities not found'}), 404

        return jsonify([ActivitySchema().dump(x) for x in data])
        
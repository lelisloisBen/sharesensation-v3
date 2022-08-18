from api import api
from database import Category
from flask_restx import Resource
from flask import jsonify
from api.schema.Category import CategorySchema

category_ns = api.namespace("category", validate=True)


@category_ns.route("/")
class CategoryListAPI(Resource):
    def get(self, *args, **kwargs):
        """
        Get registered category list
        """
        data = Category.query.all()

        if not data:
            return jsonify({'msg':'Categories not found'}), 404

        return jsonify([CategorySchema().dump(catg) for catg in data])
        
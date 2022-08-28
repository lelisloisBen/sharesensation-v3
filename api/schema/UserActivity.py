from database import ma
from database.model.UserActivity import UserActivity
from database.model.UserActivityPrice import UserActivityPrice
from database.model.UserActivityTime import UserActivityTime
from marshmallow import fields


class UserActivityPriceSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserActivityPrice
        excludes = ("id", "user_activity_id")


class UserActivityTimeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserActivityTime
        excludes = ("id", "user_activity_id")


class UserActivitySchema(ma.SQLAlchemyAutoSchema):
    """Make User object as serializable"""

    prices = fields.Method("get_prices")

    times = fields.Method("get_times")

    def get_prices(self, obj):
        prices = UserActivityPrice.query.filter_by(user_activity_id=obj.id).all()
        return UserActivityPriceSchema().dump(prices, many=True)

    def get_times(self, obj):
        times = UserActivityTime.query.filter_by(user_activity_id=obj.id).all()
        return UserActivityTimeSchema().dump(times, many=True)

    class Meta:
        model = UserActivity

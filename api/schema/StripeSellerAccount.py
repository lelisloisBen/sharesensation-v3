from database import ma, StripeSellerAccount
from marshmallow import fields
from database.model.User import User


class StripeSellerAccountSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = StripeSellerAccount

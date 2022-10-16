from api import api
from api.schema.StripeSellerAccount import StripeSellerAccountSchema
from api.utils.stripe_payment import create_seller_account
from database import StripeSellerAccount, db
from flask import current_app as app
from flask import jsonify, redirect, request
from flask_restx import Resource

from .auth import token_required

payment_ns = api.namespace("payment", validate=True)


@payment_ns.route("/seller/connected")
class PaymentAPI(Resource):
    @token_required
    def get(self, user, *args, **kwargs):
        """Check if seller account is connected"""
        seller = StripeSellerAccount.query.filter_by(user_id=user.id).first()
        if seller and seller.connected:
            return {"connected": True}, 200
        else:
            url = create_seller_account(user, seller)
            return {
                "connected": False,
                "url": url,
            }, 200


@payment_ns.route("/seller/success")
class PaymentAPI(Resource):
    def get(self, *args, **kwargs):
        seller_id = request.args.get("token", None)
        seller = StripeSellerAccount.query.filter_by(id=seller_id).first_or_404()
        seller.connected = True
        db.session.commit()
        return redirect(app.config["FRONTEND_URL"] + "/list-your-activity")

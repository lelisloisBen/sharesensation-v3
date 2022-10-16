from flask import current_app as app
import stripe
from database import StripeSellerAccount, db

stripe.api_key = app.config["STRIPE_PRIVATE_KEY"]

def create_seller_account(user, seller):
    if not seller:
        stripe_account = stripe.Account.create(type="express", email=user.email)
        seller = StripeSellerAccount(user_id=user.id, stripe_account_id=stripe_account.id)
        db.session.add(seller)
        db.session.commit()

    account_link = stripe.AccountLink.create(
        account=seller.stripe_account_id,
        refresh_url=app.config["FRONTEND_URL"],
        return_url=app.config["BACKEND_URL"] + f"/api/payment/seller/success?token={seller.id}",
        type="account_onboarding",
    )

    return account_link.url
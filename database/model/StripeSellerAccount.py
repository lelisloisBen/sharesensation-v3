from database import db

class StripeSellerAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    stripe_account_id = db.Column(db.String(40))
    connected = db.Column(db.Boolean, default=False)
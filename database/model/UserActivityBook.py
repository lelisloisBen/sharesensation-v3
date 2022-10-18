from database import db

class UserActivityBook(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    activity_id = db.Column(db.Integer, nullable=False)
    price_id = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)
    payment_intent_id = db.Column(db.String(40), nullable=False)
    paid = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<UserActivityBook %r>' % self.id

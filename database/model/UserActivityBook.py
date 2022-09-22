from database import db

class UserActivityBook(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    activity_id = db.Column(db.Integer, nullable=False)
    price_id = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return '<UserActivityBook %r>' % self.id

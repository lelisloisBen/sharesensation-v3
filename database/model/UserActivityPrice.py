from database import db

class UserActivityPrice(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_activity_id = db.Column(db.Integer, nullable=False)
    apply_index = db.Column(db.Integer, default=0, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    people_per_session = db.Column(db.Integer, nullable=False)
    duration_session = db.Column(db.Integer, nullable=False)
    detail = db.Column(db.String(255), nullable=False)
    
    def __repr__(self):
        return '<UserActivityPrice %r>' % self.id

from database import db

class UserActivityTime(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_activity_id = db.Column(db.Integer, nullable=False)
    day = db.Column(db.Integer, nullable=False) # 0~6 0:sunday, 6:saturday
    start_time = db.Column(db.String(15), nullable=False)
    end_time = db.Column(db.String(15), nullable=False)
    
    def __repr__(self):
        return '<UserActivityTime %r>' % self.id

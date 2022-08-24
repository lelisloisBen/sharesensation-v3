from database import db

class UserActivity(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    activity_id = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(30), nullable=False)
    state = db.Column(db.String(30), nullable=False)
    zipcode = db.Column(db.String(10), nullable=False)

    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    note = db.Column(db.Text, nullable=False)

    cancelation = db.Column(db.String(20), nullable=False)
    deposit = db.Column(db.Float, nullable=True)
    reservation = db.Column(db.String(20), nullable=False)
    requirement_info = db.Column(db.Text, nullable=False)

    languages = db.Column(db.JSON, nullable=False)
    equipments = db.Column(db.JSON, nullable=False)
    transportation = db.Column(db.Boolean, default=False, nullable=False)
    transportation_from = db.Column(db.String(50), nullable=True)
    transportation_to = db.Column(db.String(50), nullable=True)
    min_age = db.Column(db.Integer, nullable=True)
    max_age = db.Column(db.Integer, nullable=True)
    min_height = db.Column(db.Integer, nullable=True)
    max_height = db.Column(db.Integer, nullable=True)
    min_weight = db.Column(db.Integer, nullable=True)
    max_weight = db.Column(db.Integer, nullable=True)
    procedure_rules = db.Column(db.Text, nullable=True)

    images = db.Column(db.JSON, nullable=True)

    def __repr__(self):
        return '<UserActivity %r>' % self.id

from database import db

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    path = db.Column(db.String(120))

    def __repr__(self):
        return '<Category %r>' % self.cat

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "path": self.path,
        }
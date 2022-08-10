from database import db

class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cat =  db.Column(db.String(120))
    name = db.Column(db.String(120))
    path = db.Column(db.String(120))

    def __repr__(self):
        return '<Activity %r>' % self.cat

    def serialize(self):
        return {
            "id": self.id,
            "cat": self.cat,
            "name": self.name,
            "path": self.path
        }
from database import db

class SaleTax(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    country =  db.Column(db.String(100))
    state = db.Column(db.String(100))
    letters = db.Column(db.String(100))
    rate = db.Column(db.String(220))

    def __repr__(self):
        return '<SaleTax %r>' % self.country

    def serialize(self):
        return {
            "id": self.id,
            "country": self.country,
            "state": self.state,
            "letters": self.letters,
            "rate": self.rate
        }
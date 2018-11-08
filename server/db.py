from __init__ import db

# how can I import from csv?? do I even need to do this?

class Trips(db.Model):
    __tablename__ = 'trips'

    id = db.Column(db.Integer, primary_key=True)

    def __init__(self):
        return self

    def __repr__(self):
        return '<id {}>'.format(self.id)



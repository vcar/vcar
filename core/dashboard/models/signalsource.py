from datetime import datetime
from ...extensions import db

# -------------------------------- Signalsource Model ----------------------- #


class Signalsource(db.Model):
    """ Signalsource Model: """
    __tablename__ = 'signalsources'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.String(1000))
    signals = db.relationship("Signal")

    status = db.Column(db.SmallInteger, default=1)
    created = db.Column(db.DateTime(), default=datetime.utcnow())

    def __init__(self, name, description, status=1):
        self.name = name
        self.status = status
        self.description = description

    def __repr__(self):
        return str(self.name)

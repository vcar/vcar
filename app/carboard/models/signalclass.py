from datetime import datetime
from ...extensions import db

# -------------------------------- Signalclass Model ------------------------------- #


class Signalclass(db.Model):
    """ Signalclass Model: """
    __tablename__ = 'signalclasses'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

    signals = db.relationship("Signal")

    status = db.Column(db.SmallInteger, default=1)
    created = db.Column(db.DateTime(), default=datetime.utcnow())

    def __init__(self, name, status=1):
        self.name = name
        self.status = status

    def __repr__(self):
        return str(self.name)

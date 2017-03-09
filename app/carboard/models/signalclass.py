from ..constants import STRING_LEN, ACTIVE
from ..helpers import get_current_time
from ...extensions import db

# -------------------------------- Signalclass Model ------------------------------- #


class Signalclass(db.Model):
    """ Signalclass Model: """
    __tablename__ = 'signalclasses'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(STRING_LEN))

    signals = db.relationship("Signal")

    status = db.Column(db.SmallInteger, default=ACTIVE)
    created = db.Column(db.DateTime(), default=get_current_time())

    def __init__(self, name, status=ACTIVE):
        self.name = name
        self.status = status

    def __repr__(self):
        return str(self.name)

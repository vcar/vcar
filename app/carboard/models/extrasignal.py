from ..constants import STRING_LEN, ACTIVE
from ..helpers import get_current_time
from ...extensions import db

# -------------------------------- Extrasignal Model ------------------------------- #


class Extrasignal(db.Model):
    """ Extrasignal Model: """
    __tablename__ = 'extrasignals'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(STRING_LEN))

    signal_id = db.Column(db.Integer, db.ForeignKey('signals.id'))
    signal = db.relationship("Signal", back_populates="extrasignals")

    platform_id = db.Column(db.Integer, db.ForeignKey('platforms.id'))
    platform = db.relationship('Platform', back_populates="signals")

    status = db.Column(db.SmallInteger, default=ACTIVE)
    created = db.Column(db.DateTime(), default=get_current_time())

    def __init__(self, name, signal_id, platform_id, status=ACTIVE):
        self.name = name
        self.signal_id = signal_id
        self.platform_id = platform_id
        self.status = status

    def __repr__(self):
        return str(self.name)

from datetime import datetime
from marshmallow import Schema, fields
from .signal import SignalSchema
from ...extensions import db

# -------------------------------- Extrasignal Model ------------------------------- #


class Extrasignal(db.Model):
    """ Extrasignal Model: """
    __tablename__ = 'extrasignals'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

    signal_id = db.Column(db.Integer, db.ForeignKey('signals.id'))
    signal = db.relationship("Signal", back_populates="extrasignals")

    platform_id = db.Column(db.Integer, db.ForeignKey('platforms.id'))
    platform = db.relationship('Platform', back_populates="signals")

    status = db.Column(db.SmallInteger, default=1)
    created = db.Column(db.DateTime(), default=datetime.utcnow())

    def __init__(self, name, signal_id, platform_id, status=1):
        self.name = name
        self.signal_id = signal_id
        self.platform_id = platform_id
        self.status = status

    def __repr__(self):
        return str(self.name)

# -------------------------------- Extrasignal Model ------------------------------- #


class ExtrasignalSchema(Schema):
    """ Extra signals schema """

    id = fields.Int(dump_only=True)
    name = fields.Str()
    signal = fields.Nested(SignalSchema)

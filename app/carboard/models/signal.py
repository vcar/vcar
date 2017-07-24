from datetime import datetime
from marshmallow import Schema, fields
from ...extensions import db


# -------------------------------- Signal Model ------------------------------- #


class Signal(db.Model):
    """ Signal Model: """
    __tablename__ = 'signals'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.String(1000))
    type = db.Column(db.String(100))
    range = db.Column(db.String(255))
    frequency = db.Column(db.String(255))
    unit = db.Column(db.String(255))

    extrasignals = db.relationship("Extrasignal")

    signalclass_id = db.Column(db.Integer, db.ForeignKey('signalclasses.id'))
    signalclass = db.relationship("Signalclass", back_populates="signals")

    signalsource_id = db.Column(db.Integer, db.ForeignKey('signalsources.id'))
    signalsource = db.relationship("Signalsource", back_populates="signals")

    status = db.Column(db.SmallInteger, default=1)
    created = db.Column(db.DateTime(), default=datetime.utcnow())

    def __init__(self, name, signalclass_id, signalsource_id, frequency, type, description, unit, status=1 ):
        self.name = name
        self.signalclass_id = signalclass_id
        self.signalsource_id = signalsource_id
        self.status = status
        self.frequency = frequency
        self.type = type
        self.description = description
        self.unit = unit

    def __repr__(self):
        return str(self.name)


# -------------------------------- Signal Model ----------------------------- #


class SignalSchema(Schema):
    """ Extra signals schema """

    id = fields.Int(dump_only=True)
    name = fields.Str()
    signalclass = fields.Str()
    signalsource = fields.Str()

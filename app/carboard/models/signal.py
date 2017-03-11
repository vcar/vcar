from marshmallow import Schema, fields
from ..constants import STRING_LEN, ACTIVE
from ..helpers import get_current_time
from ...extensions import db

# -------------------------------- Signal Model ------------------------------- #


class Signal(db.Model):
    """ Signal Model: """
    __tablename__ = 'signals'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(STRING_LEN))

    extrasignals = db.relationship("Extrasignal")

    signalclass_id = db.Column(db.Integer, db.ForeignKey('signalclasses.id'))
    signalclass = db.relationship("Signalclass", back_populates="signals")

    status = db.Column(db.SmallInteger, default=ACTIVE)
    created = db.Column(db.DateTime(), default=get_current_time())

    def __init__(self, name, signalclass_id, status=ACTIVE):
        self.name = name
        self.signalclass_id = signalclass_id
        self.status = status

    def __repr__(self):
        return str(self.name)




# -------------------------------- Signal Model ----------------------------- #


class SignalSchema(Schema):
    """ Extra signals schema """

    id = fields.Int(dump_only=True)
    name = fields.Str()
    signalclass = fields.Str()

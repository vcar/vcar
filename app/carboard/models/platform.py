from marshmallow import Schema, fields
from .extrasignal import ExtrasignalSchema
from ..constants import STRING_LEN, ACTIVE
from ..helpers import get_current_time, slugify
from ...extensions import db

# -------------------------------- Brand Model ------------------------------- #


class Platform(db.Model):
    """ Platform Model """
    __tablename__ = 'platforms'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(STRING_LEN))
    slug = db.Column(db.String(STRING_LEN))
    logo = db.Column(db.String(STRING_LEN), nullable=True)
    description = db.Column(db.String(STRING_LEN))
    website = db.Column(db.String(STRING_LEN), nullable=True)

    signals = db.relationship("Extrasignal")

    status = db.Column(db.SmallInteger, default=ACTIVE)
    created = db.Column(db.DateTime(), default=get_current_time())

    def __init__(self, name, description, website, logo=None):
        self.name = name
        self.slug = slugify(name)
        self.logo = logo
        self.description = description
        self.website = website

    def __repr__(self):
        return self.name

# -------------------------------- Brand Schema ------------------------------- #


class PlatformSchema(Schema):
    """ Platform Schema """

    id = fields.Int(dump_only=True)
    name = fields.Str()
    slug = fields.Str()
    logo = fields.Str()
    signals = fields.Nested(ExtrasignalSchema)
    description = fields.Str()
    website = fields.Str()
    created = fields.DateTime(dump_only=True)

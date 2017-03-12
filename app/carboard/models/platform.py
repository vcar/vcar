from datetime import datetime
from marshmallow import Schema, fields
from .extrasignal import ExtrasignalSchema
from ..constants import DEFAULT_PHOTO
from ..helpers import slugify
from ...extensions import db

# -------------------------------- Brand Model ------------------------------- #


class Platform(db.Model):
    """ Platform Model """
    __tablename__ = 'platforms'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    slug = db.Column(db.String(255))
    logo = db.Column(db.String(255), nullable=True)
    description = db.Column(db.String(255))
    website = db.Column(db.String(255), nullable=True)

    signals = db.relationship("Extrasignal")

    status = db.Column(db.SmallInteger, default=1)
    created = db.Column(db.DateTime(), default=datetime.utcnow())

    def __init__(self, name, description, website, logo=None):
        self.name = name
        self.slug = slugify(name)
        self.logo = logo or DEFAULT_PHOTO
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

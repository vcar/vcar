import re
from datetime import datetime
from unicodedata import normalize

from marshmallow import Schema, fields
from .extrasignal import ExtrasignalSchema
from ..constants import DEFAULT_PHOTO
from ...extensions import db

# -------------------------------- Brand Model ------------------------------- #
def slugify(text, delim=u'-'):
    """Generates an slightly worse ASCII-only slug."""
    result = []
    _punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')
    for word in _punct_re.split(text.lower()):
        word = normalize('NFKD', word).encode('ascii', 'ignore')
        if word:
            result.append(word)
    try:
        return unicode(delim.join(result))
    except:
        d = d = bytes(delim, 'utf-8')
        return str(d.join(result).decode("utf-8"))

class Platform(db.Model):
    """ Platform Model """
    __tablename__ = 'platforms'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    slug = db.Column(db.String(255))
    mimetype = db.Column(db.SmallInteger)
    logo = db.Column(db.String(255), nullable=True)
    description = db.Column(db.String(255))
    website = db.Column(db.String(255), nullable=True)

    #signals = db.relationship("Extrasignal")

    status = db.Column(db.SmallInteger, default=1)
    created = db.Column(db.DateTime(), default=datetime.utcnow())

    def __init__(self, name, mimetype, description, website, logo=None):
        self.name = name
        self.slug = slugify(name)
        self.mimetype = mimetype
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
    mimetype = fields.Str()
    logo = fields.Str()
    signals = fields.Nested(ExtrasignalSchema)
    description = fields.Str()
    website = fields.Str()
    created = fields.DateTime(dump_only=True)

from datetime import datetime
from ..helpers.helpers import slugify
from ...extensions import db

# -------------------------------- Brand Model ------------------------------- #


class Brand(db.Model):
    """ Brand (Marque) Model """
    __tablename__ = 'brands'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    slug = db.Column(db.String(255))
    logo = db.Column(db.String(255), nullable=True)
    code = db.Column(db.String(255))
    status = db.Column(db.SmallInteger, default=1)
    created = db.Column(db.DateTime(), default=datetime.utcnow())

    def __init__(self, name, code, logo=None):
        self.name = name
        self.slug = slugify(name)
        self.code = code
        self.logo = logo

    def __repr__(self):
        return self.name

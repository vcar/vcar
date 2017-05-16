from datetime import datetime
from ..helpers import slugify
from ...extensions import db

# -------------------------------- Brand Model ------------------------------ #


class Dataset(db.Model):
    """ Dataset Model """
    __tablename__ = 'datasets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    slug = db.Column(db.String(255))
    description = db.Column(db.String(255))
    author = db.Column(db.String(255), nullable=True)
    lab = db.Column(db.String(255), nullable=True)
    website = db.Column(db.String(255), nullable=True)

    article = db.relationship("Article", uselist=False, back_populates="dataset")

    status = db.Column(db.SmallInteger, default=1)
    created = db.Column(db.DateTime(), default=datetime.utcnow())

    def __init__(self, name, description, slug=None, author=None, lab=None, website=None):
        self.name = name
        self.slug = slug if slug != '' else slugify(name, '_')
        self.description = description
        self.author = author
        self.lab = lab
        self.website = website

    def __repr__(self):
        return self.name

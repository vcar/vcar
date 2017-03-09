from ..constants import STRING_LEN, ACTIVE
from ..helpers import get_current_time, slugify
from ...extensions import db

# -------------------------------- Brand Model ------------------------------ #


class Dataset(db.Model):
    """ Dataset Model """
    __tablename__ = 'datasets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(STRING_LEN))
    slug = db.Column(db.String(STRING_LEN))
    description = db.Column(db.String(STRING_LEN))
    author = db.Column(db.String(STRING_LEN), nullable=True)
    lab = db.Column(db.String(STRING_LEN), nullable=True)
    website = db.Column(db.String(STRING_LEN), nullable=True)

    article = db.relationship("Article", uselist=False, back_populates="dataset")

    status = db.Column(db.SmallInteger, default=ACTIVE)
    created = db.Column(db.DateTime(), default=get_current_time())

    def __init__(self, name, description, author=None, lab=None, website=None):
        self.name = name
        self.slug = slugify(name, '_')
        self.description = description
        self.author = author
        self.lab = lab
        self.website = website

    def __repr__(self):
        return self.name

from ..constants import STRING_LEN, ACTIVE
from ..helpers import get_current_time, slugify
from ...extensions import db

# -------------------------------- Brand Model ------------------------------- #


class Brand(db.Model):
    """ Brand (Marque) Model """
    __tablename__ = 'brands'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(STRING_LEN))
    slug = db.Column(db.String(STRING_LEN))
    logo = db.Column(db.String(STRING_LEN), nullable=True)
    code = db.Column(db.String(STRING_LEN))
    status = db.Column(db.SmallInteger, default=ACTIVE)
    created = db.Column(db.DateTime(), default=get_current_time())

    def __init__(self, name, code, logo=None):
        self.name = name
        self.slug = slugify(name)
        self.code = code
        self.logo = logo

    def __repr__(self):
        return self.name

from ..constants import STRING_LEN, ACTIVE
from ..helpers import get_current_time
from ...extensions import db

# -------------------------------- Driver Model ------------------------------- #


class Country(db.Model):
    """ Country Model """
    __tablename__ = 'countries'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(STRING_LEN), index=True)
    code = db.Column(db.String(STRING_LEN))
    status = db.Column(db.SmallInteger, default=ACTIVE)
    created = db.Column(db.DateTime(), default=get_current_time())


    def __init__(self, title, code):
        self.title = title
        self.code = code

    def __repr__(self):
        return self.title

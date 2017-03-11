from datetime import datetime
from ...extensions import db

# -------------------------------- Driver Model ------------------------------- #


class Country(db.Model):
    """ Country Model """
    __tablename__ = 'countries'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), index=True)
    code = db.Column(db.String(255))
    status = db.Column(db.SmallInteger, default=1)
    created = db.Column(db.DateTime(), default=datetime.utcnow())


    def __init__(self, title, code):
        self.title = title
        self.code = code

    def __repr__(self):
        return self.title

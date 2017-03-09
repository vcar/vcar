from uuid import uuid4

from .constants import STRING_LEN, PROCESSED, NOT_PROCESSED
from .helpers import get_current_time
from ..extensions import db

# -------------------------------- Trace Model ------------------------------ #


class Trace(db.Model):

    __tablename__ = 'traces'

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(STRING_LEN))
    path = db.Column(db.String(STRING_LEN), nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    processed = db.Column(db.SmallInteger, default=NOT_PROCESSED)
    created = db.Column(db.DateTime(), default=get_current_time())
    user = db.relationship('User', backref=db.backref('traces', lazy='dynamic'))

    def __init__(self, user_id, filename=None, path=None, processed=NOT_PROCESSED):
        self.filename = filename
        self.path = path
        self.user_id = user_id
        self.processed = processed

    def is_processed(self):
        return self.processed == PROCESSED

    def __repr__(self):
        return '<Trace {}>'.format(self.filename)

    @classmethod
    def get_by_user_id(cls, user_id, processed=NOT_PROCESSED):
        return cls.query.filter(
            Trace.user_id == user_id and Trace.processed == processed
        ).all()
# (db.session.query(Address).filter_by(person_id=current_user.id).count())
# -------------------------------- Trace Model ------------------------------ #

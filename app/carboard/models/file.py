from uuid import uuid4
from ..constants import STRING_LEN, PROCESSED, NOT_PROCESSED
from ..helpers import get_current_time
from ...extensions import db


# ------------------------------ File Model -------------------------------- #


class File(db.Model):

    __tablename__ = 'files'

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('files', lazy='dynamic'))

    filename = db.Column(db.String(STRING_LEN))
    path = db.Column(db.String(STRING_LEN), nullable=False, unique=True)
    processed = db.Column(db.SmallInteger, default=NOT_PROCESSED)
    created = db.Column(db.DateTime(), default=get_current_time())

    def __init__(self, user_id, filename=None, path=None, processed=NOT_PROCESSED):
        self.filename = filename
        self.path = path
        self.user_id = user_id
        self.processed = processed

    def is_processed(self):
        return self.processed == PROCESSED

    def __repr__(self):
        return '<File {}>'.format(self.filename)

    @classmethod
    def get_by_user_id(cls, user_id, processed=NOT_PROCESSED):
        return cls.query.filter(
            File.user_id == user_id and File.processed == processed
        ).all()

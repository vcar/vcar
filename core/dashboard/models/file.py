from uuid import uuid4
from datetime import datetime
from ...extensions import db


# ------------------------------ File Model -------------------------------- #


class File(db.Model):

    __tablename__ = 'files'

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('files', lazy='dynamic'))

    filename = db.Column(db.String(255))
    path = db.Column(db.String(255), nullable=False, unique=True)
    processed = db.Column(db.SmallInteger, default=0)
    created = db.Column(db.DateTime(), default=datetime.utcnow())

    def __init__(self, user_id, filename=None, path=None, processed=0):
        self.filename = filename
        self.path = path
        self.user_id = user_id
        self.processed = processed

    def is_processed(self):
        return self.processed == 1

    def __repr__(self):
        return '<File {}>'.format(self.filename)

    @classmethod
    def get_by_user_id(cls, user_id, processed=0):
        return cls.query.filter(
            File.user_id == user_id and File.processed == processed
        ).all()

from datetime import datetime
from ...extensions import db

# -------------------------------- Driver Model ------------------------------- #


class Driver(db.Model):
    """ Driver Model:
        The driver is the one who produce data records.
    """
    __tablename__ = 'drivers'

    id = db.Column(db.Integer, primary_key=True)
    gender = db.Column(db.SmallInteger, default=0)
    fullname = db.Column(db.String(255), default='Anonyme')
    avatar = db.Column(db.String(255), nullable=True)
    city = db.Column(db.String(255), nullable=True)

    status_id = db.Column(db.SmallInteger, db.ForeignKey('status.id'))
    status = db.relationship('Status')

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', backref=db.backref('drivers', lazy='dynamic'))

    country_id = db.Column(db.Integer, db.ForeignKey('countries.id'))
    country = db.relationship('Country')

    created = db.Column(db.DateTime(), default=datetime.utcnow())

    def __init__(self, user_id, country_id, **kwargs):
        self.vars = kwargs
        self.gender = kwargs.get('gender', 3)
        self.fullname = kwargs.get('fullname', 'Anonymous driver')
        self.user_id = user_id
        self.country_id = country_id
        self.avatar = kwargs.get('avatar')
        self.status_id = kwargs.get('status_id', 1)
        self.city = kwargs.get('city')

    def __repr__(self):
        return self.fullname
